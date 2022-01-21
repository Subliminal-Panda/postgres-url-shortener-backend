from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt

import psycopg2
import os
import random
import string

app = Flask(__name__)
bcrypt = Bcrypt(app)

front_end = "https://tm57.herokuapp.com/"
# front_end = "http://localhost:3000/"

api_v1_cors_config = {
    "origins": [front_end, "*"]
}

CORS(app, resources={
    r"/*": api_v1_cors_config
})
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://wmmkxwfjbkfgae:c81ac8f539fa168b3e6e2575be7ef7dabdac4ece4938ee4ca87cd86a5887d73a@ec2-54-157-15-228.compute-1.amazonaws.com:5432/d6nn4l84c8d1kc"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)

# creates link class

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.String, nullable=False)
    stored_url = db.Column(db.String, nullable=False)
    stored_link = db.Column(db.String, nullable=False)

    def __init__(self, created_by, stored_url, stored_link):
        self.created_by = created_by
        self.stored_url = stored_url
        self.stored_link = stored_link

# sets up the schema for the database:

class LinkSchema(ma.Schema):
    class Meta:
        fields = ('id', 'created_by', 'stored_url', 'stored_link')

link_schema = LinkSchema()
multiple_link_schema = LinkSchema(many=True)

# creates user class:

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    logged_in = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, password, logged_in):
        self.username = username
        self.password = password
        self.logged_in = logged_in

# sets up user schema for database:

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'logged_in')

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)



# checks database for active login session for user:

@app.route('/app/user/sessions', methods=['PATCH'])
@cross_origin()
def find_session():
    if request.content_type != 'application/json':
        return jsonify("Error: Data must be formatted as JSON.")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    user = db.session.query(User).filter(User.username == username).first()


    if user is not None:
        if bcrypt.check_password_hash(user.password, password) == True:
            user.logged_in = True
            return jsonify("created")
        else:
            return jsonify("incorrect password")

    else:
        return jsonify("user not found")

@app.route('/app/user/add', methods=['POST'])
@cross_origin()
def add_user():
    if request.content_type != 'application/json':
        return jsonify("Error: Data must be formatted as JSON.")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")
    logged_in = True

    possible_duplicate = db.session.query(User).filter(User.username == username).first()

    if possible_duplicate is not None:
        return jsonify('That username is taken')

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username, encrypted_password, logged_in)

    db.session.add(new_user)
    db.session.commit()

    return jsonify('New user created')

@app.route('/app/user/get', methods=['GET'])
@cross_origin()
def get_users():
    all_users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(all_users))

@app.route('/app/user/get/<id>', methods=['GET'])
@cross_origin()
def get_user_by_id(id):
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dump(user))

@app.route('/app/user/get/username/<username>', methods=['GET'])
@cross_origin()
def get_user_by_username(username):
    user = db.session.query(User).filter(User.username == username).first()
    return jsonify(user_schema.dump(user))

@app.route('/app/auth/<user>', methods=['GET'])
@cross_origin()
def login_status(user):
    user_to_verify = db.session.query(User).filter(User.username == user).first()
    return jsonify(user_schema.dump(user_to_verify))

# route to add a new link:

@app.route('/app/links', methods=['POST'])
@cross_origin()
def add_link():
    if request.content_type != 'application/json':
        return jsonify("Error: Data must be formatted as JSON.")

    post_data = request.get_json()
    created_by = post_data.get("created_by")
    stored_url = post_data.get("stored_url")
    stored_link = post_data.get("stored_link")

    if stored_link == "":

        # generate random short link:

        saved_link = "".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7)])
        possible_duplicate = db.session.query(Link).filter(Link.stored_link == saved_link).first()

        # check for duplicates, re-generate random link until no duplicates are found:

        while possible_duplicate is not None:
            saved_link = "".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7)])
            possible_duplicate = db.session.query(Link).filter(Link.stored_link == saved_link).first()

    # saves user input as short link, if it exists:

    else:
        possible_duplicate = db.session.query(Link).filter(Link.stored_link == stored_link).first()
        if possible_duplicate is not None:
            return jsonify("Error: that link is already being used.", stored_link)

        saved_link = stored_link

        # stores new link/url data in a variable, and saves it in the database:

    new_link = Link(created_by, stored_url, saved_link)

    db.session.add(new_link)
    db.session.commit()

    successful = ["New link added to database:", created_by, stored_url, saved_link]
    return jsonify(successful)

# route to retrieve all links:




@app.route('/app/user/links/<user>', methods=['GET'])
@cross_origin()
def get_user_links(user):
    user_links = db.session.query(Link).filter(Link.created_by == user)
    return jsonify(multiple_link_schema.dump(user_links))

# route to retrieve one link:

@app.route('/app/links/<link>', methods=['GET'])
@cross_origin()
def get_link(link):
    found_link = db.session.query(Link).filter(Link.stored_link == link).first()
    print("stored url:", found_link.stored_url)
    return jsonify(link_schema.dump(found_link))

# route to delete one link by its unique id:

@app.route('/app/links/<link>', methods=['DELETE'])
@cross_origin()
def delete_link(link):
    link_to_delete = db.session.query(Link).filter(Link.id == link).first()
    db.session.delete(link_to_delete)
    db.session.commit()
    successful = ["The following link has been deleted:", link_schema.dump(link_to_delete)]
    return jsonify(successful)

@app.route('/app/links', methods=['GET'])
@cross_origin()
def get_all_links():
    all_links = db.session.query(Link).all()
    return jsonify(multiple_link_schema.dump(all_links))

@app.route('/<link>')
@cross_origin()
def direct(link):
    direct_url = db.session.query(Link).filter(Link.stored_link == link).first()
    if direct_url is not None:
        if direct_url.stored_url.startswith('http://') or direct_url.stored_url.startswith('https://'):
            parsed_url = direct_url.stored_url
        else:
            parsed_url = 'https://' + direct_url.stored_url
        return redirect(parsed_url, code=301)
    else:
        return redirect(front_end, code=301)

@app.route('/')
@cross_origin()
def go_to_home():
    return redirect(front_end, code=301)

@app.route('/app')
@cross_origin()
def go_to_front():
    return redirect(front_end, code=301)

if __name__ == "__main__":
    app.run(debug=True)
