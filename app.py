from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import psycopg2
import os

import random
import string

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://wmmkxwfjbkfgae:c81ac8f539fa168b3e6e2575be7ef7dabdac4ece4938ee4ca87cd86a5887d73a@ec2-54-157-15-228.compute-1.amazonaws.com:5432/d6nn4l84c8d1kc"
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

# creates link class and

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stored_url = db.Column(db.String, nullable=False)
    stored_link = db.Column(db.String, nullable=False)

    def __init__(self, stored_url, stored_link):
        self.stored_url = stored_url
        self.stored_link = stored_link

# sets up the schema for the database:

class LinkSchema(ma.Schema):
    class Meta:
        fields = ('id', 'stored_url', 'stored_link')

link_schema = LinkSchema()
multiple_link_schema = LinkSchema(many=True)

# route to add a new link:

@app.route('/url/add', methods=['POST'])
def add_link():
    if request.content_type != 'application/json':
        return jsonify("Error: Data must be formatted as JSON.")

    post_data = request.get_json()
    stored_url = post_data.get("stored_url")
    stored_link = post_data.get("stored_link")

    if stored_link == "":

        # generate random short link:

        saved_link = "".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)])
        possible_duplicate = db.session.query(Link).filter(Link.stored_link == saved_link).first()

        # check for duplicates, re-generate random link until no duplicates are found:

        while possible_duplicate is not None:
            saved_link = "".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)])
            possible_duplicate = db.session.query(Link).filter(Link.stored_link == saved_link).first()

    # saves user input as short link, if it exists:

    else:
        saved_link = stored_link

    # stores new link/url data in a variable, and saves it in the database:

    new_link = Link(stored_url, saved_link)

    db.session.add(new_link)
    db.session.commit()

    successful = ["New link added to database:", link_schema.dump(new_link)]
    return jsonify(successful)

# route to retrieve all links:

@app.route('/url/get', methods=["GET"])
def get_all_links():
    all_links = db.session.query(Link).all()
    return jsonify(multiple_link_schema.dump(all_links))

# route to retrieve one link:

@app.route('/url/get/link/<link>', methods=["GET"])
def get_link(link):
    found_link = db.session.query(Link).filter(Link.stored_link == link).first()
    return jsonify(link_schema.dump(found_link))

# route to delete one link by its shortlink name:

@app.route("/url/delete/<link>", methods=['DELETE'])
def delete_link(link):
    link = db.session.query(Link).filter(Link.stored_link == link).first()
    db.session.delete(link)
    db.session.commit()
    successful = ["The following link has been deleted:", link_schema.dump(link)]
    return jsonify(successful)

# route to delete one link by its unique id:

@app.route("/url/delete/id/<id>", methods=['DELETE'])
def delete_link_by_id(id):
    link_by_id = db.session.query(Link).filter(Link.id == id).first()
    db.session.delete(link_by_id)
    db.session.commit()
    successful = ["The following link has been deleted:", link_schema.dump(link_by_id)]
    return jsonify(successful)

if __name__ == "__main__":
    app.run(debug=True)
