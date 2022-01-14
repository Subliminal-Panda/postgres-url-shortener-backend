from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import psycopg2
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://yscghqqerxizxq:fa0b50341d56eef162e9f5e13bc7b718274f7ff10f2419e525de2f05bf1fa7c9@ec2-34-195-69-118.compute-1.amazonaws.com:5432/d3ribmkrmp9us1"
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
bcrypt = Bcrypt(app)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stored_url = db.Column(db.String, nullable=False)
    stored_link = db.Column(db.String, nullable=False)

    def __init__(self, stored_url, stored_link):
        self.stored_url = stored_url
        self.stored_link = stored_link

class LinkSchema(ma.Schema):
    class Meta:
        fields = ('id', 'stored_url', 'stored_link')

link_schema = LinkSchema()
multiple_link_schema = LinkSchema(many=True)

@app.route('/url/add', methods=['POST'])
def add_url():
    if request.content_type != 'application/json':
        return jsonify("Error: Data must be formatted as JSON.")

    post_data = request.get_json()
    stored_url = post_data.get("url")
    stored_link = post_data.get("custom link")

    new_link = Link(stored_url, stored_link)

    db.session.add(new_link)
    db.session.commit()

    successful = ["New link added to database:", link_schema.dump(new_link)]
    return jsonify(successful)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    chess_checkmate_wins = db.Column(db.Integer, nullable=False)
    chess_resignation_wins = db.Column(db.Integer, nullable=False)
    chess_timeout_wins = db.Column(db.Integer, nullable=False)
    chess_checkmate_losses = db.Column(db.Integer, nullable=False)
    chess_resignation_losses = db.Column(db.Integer, nullable=False)
    chess_timeout_losses = db.Column(db.Integer, nullable=False)
    chess_stalemate_draws = db.Column(db.Integer, nullable=False)
    chess_insufficient_material_draws = db.Column(db.Integer, nullable=False)
    chess_fifty_move_draws = db.Column(db.Integer, nullable=False)
    chess_repetition_draws = db.Column(db.Integer, nullable=False)
    chess_agreement_draws = db.Column(db.Integer, nullable=False)



    def __init__(self, username, password, chess_checkmate_wins, chess_resignation_wins, chess_timeout_wins, chess_checkmate_losses, chess_resignation_losses, chess_timeout_losses, chess_stalemate_draws, chess_insufficient_material_draws, chess_fifty_move_draws, chess_repetition_draws, chess_agreement_draws):
        self.username = username
        self.password = password
        self.chess_checkmate_wins = chess_checkmate_wins
        self.chess_resignation_wins = chess_resignation_wins
        self.chess_timeout_wins = chess_timeout_wins
        self.chess_checkmate_losses = chess_checkmate_losses
        self.chess_resignation_losses = chess_resignation_losses
        self.chess_timeout_losses = chess_timeout_losses
        self.chess_stalemate_draws = chess_stalemate_draws
        self.chess_insufficient_material_draws = chess_insufficient_material_draws
        self.chess_fifty_move_draws = chess_fifty_move_draws
        self.chess_repetition_draws = chess_repetition_draws
        self.chess_agreement_draws = chess_agreement_draws

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'chess_checkmate_wins', 'chess_resignation_wins', 'chess_timeout_wins', 'chess_checkmate_losses', 'chess_resignation_losses', 'chess_timeout_losses', 'chess_stalemate_draws', 'chess_insufficient_material_draws', 'chess_fifty_move_draws', 'chess_repetition_draws', 'chess_agreement_draws')

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

@app.route('/user/add', methods=['POST'])
def add_user():
    if request.content_type != 'application/json':
        return jsonify("Error: Data must be formatted as JSON.")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")
    chess_checkmate_wins = 0
    chess_resignation_wins = 0
    chess_timeout_wins = 0
    chess_checkmate_losses = 0
    chess_resignation_losses = 0
    chess_timeout_losses = 0
    chess_stalemate_draws = 0
    chess_insufficient_material_draws = 0
    chess_fifty_move_draws = 0
    chess_repetition_draws = 0
    chess_agreement_draws = 0

    possible_duplicate = db.session.query(User).filter(User.username == username).first()

    if possible_duplicate is not None:
        unsuccessful = ['That username is taken.', username]
        return jsonify(unsuccessful)

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username, encrypted_password, chess_checkmate_wins, chess_resignation_wins, chess_timeout_wins, chess_checkmate_losses, chess_resignation_losses, chess_timeout_losses, chess_stalemate_draws, chess_insufficient_material_draws, chess_fifty_move_draws, chess_repetition_draws, chess_agreement_draws)

    db.session.add(new_user)
    db.session.commit()

    successful = ["New user added to database:", user_schema.dump(new_user)]
    return jsonify(successful)

@app.route('/user/verify', methods=['POST'])
def verify_user():
    if request.content_type != 'application/json':
        return jsonify("Error: Data must be formatted as JSON.")

    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')

    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return jsonify('User not found.')

    if bcrypt.check_password_hash(user.password, password) == False:
        return jsonify('Incorrect password.')

    successful = ['User verified:', user_schema.dump(user)]
    return jsonify(successful)

@app.route('/user/get', methods=['GET'])
def get_users():
    all_users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(all_users))

@app.route('/user/get/id/<id>', methods=['GET'])
def get_user_by_id(id):
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dump(user))

@app.route('/user/get/username/<username>', methods=['GET'])
def get_user_by_username(username):
    user = db.session.query(User).filter(User.username == username).first()
    return jsonify(user_schema.dump(user))

@app.route("/user/delete/<id>", methods=['DELETE'])
def delete_user_by_id(id):
    user = db.session.query(User).filter(User.id == id).first()
    db.session.delete(user)
    db.session.commit()
    successful = ["The following user account has been deleted:", user_schema.dump(user)]
    return jsonify(successful)

@app.route('/user/update/<id>', methods=['PUT'])
def update_user_by_id(id):
    if request.content_type != "application/json":
        return jsonify("Error: Data must be formatted as JSON.")

    if id == None:
        return jsonify("Error: I can't update without a user ID.")

    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')
    chess_checkmate_wins = post_data.get('chess_checkmate_wins')
    chess_resignation_wins = post_data.get('chess_resignation_wins')
    chess_timeout_wins = post_data.get('chess_timeout_wins')
    chess_checkmate_losses = post_data.get('chess_checkmate_losses')
    chess_resignation_losses = post_data.get('chess_resignation_losses')
    chess_timeout_losses = post_data.get('chess_timeout_losses')
    chess_stalemate_draws = post_data.get('chess_stalemate_draws')
    chess_insufficient_material_draws = post_data.get('chess_insufficient_material_draws')
    chess_fifty_move_draws = post_data.get('chess_fifty_move_draws')
    chess_repetition_draws = post_data.get('chess_repetition_draws')
    chess_agreement_draws = post_data.get('chess_agreement_draws')

    user = db.session.query(User).filter(User.id == id).first()

# create a secure way to update username and password

    if chess_checkmate_wins != None:
        user.chess_checkmate_wins += 1
    if chess_resignation_wins != None:
        user.chess_resignation_wins += 1
    if chess_timeout_wins != None:
        user.chess_timeout_wins += 1
    if chess_checkmate_losses != None:
        user.chess_checkmate_losses += 1
    if chess_resignation_losses != None:
        user.chess_resignation_losses += 1
    if chess_timeout_losses != None:
        user.chess_timeout_losses += 1
    if chess_stalemate_draws != None:
        user.chess_stalemate_draws += 1
    if chess_insufficient_material_draws != None:
        user.chess_insufficient_material_draws += 1
    if chess_fifty_move_draws != None:
        user.chess_fifty_move_draws += 1
    if chess_repetition_draws != None:
        user.chess_repetition_draws += 1
    if chess_agreement_draws != None:
        user.chess_agreement_draws += 1

    db.session.commit()
    successful = ["user updated:", user_schema.dump(user)]
    return jsonify(successful)


if __name__ == "__main__":
    app.run(debug=True)
