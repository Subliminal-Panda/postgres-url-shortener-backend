from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://bogyliizsxovqh:840f94a6715b0db914cf8f9e85c6cbfef5a28715a9360c45035a301d648cc82b@ec2-3-227-15-75.compute-1.amazonaws.com:5432/d82ac9nbeq3255"
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

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
    stored_url = post_data.get("stored_url")
    stored_link = post_data.get("stored_link")

    if stored_link == "_empty_":
        saved_link = "".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10)])
    else:
        saved_link = stored_link

    new_link = Link(stored_url, saved_link)

    db.session.add(new_link)
    db.session.commit()

    successful = ["New link added to database:", link_schema.dump(new_link)]
    return jsonify(successful)

if __name__ == "__main__":
    app.run(debug=True)
