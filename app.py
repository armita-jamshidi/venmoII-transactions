from datetime import datetime
import json

import db
from flask import Flask
from flask import request

#DB is DatabaseDriver object
DB = db.DatabaseDriver()

app = Flask(__name__)

#-----------USERS------------------------------------------
@app.route("/api/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    dict = {"users": DB.get_all_users()}
    return json.dumps(dict), 200

@app.route("/api/users/",methods=["POST"])
def create_user():
    """
    Endpoint for creating a user
    """
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance")

    id = DB.create_user(name, username, balance)
    user = DB.get_user_by_id(id)

    return json.dumps(user), 201

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a specific user
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User is not found!"}), 404
    return json.dumps(user), 200

@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
