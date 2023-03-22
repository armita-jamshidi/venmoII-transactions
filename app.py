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
    user["transactions"] = []

    return json.dumps(user), 201

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a specific user
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User is not found!"}), 404
    
    #adding transactions manually as a list
    user["transactions"] = DB.get_transactions_by_id(user_id)
    return json.dumps(user), 200

@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a specific user
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "user not found!"}), 404
    DB.delete_user_by_id(user_id)

    a = DB.delete_transactions_by_id(user_id)
    if a is None:
        user["transactions"] = []
    else:
        user["transactions"] = a
    return json.dumps(user), 200

@app.route("/api/send/",methods=["POST"])
def send_money():
    """
    Endpoint for sending money from one user to another
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")

    response = DB.send_money(sender_id, receiver_id, amount)
    if response is None:
        return json.dumps({"error": "sender does not have enough money in their account"}), 400
    
    return json.dumps(response), 200

@app.route("/")
def hello_world():
    return "Hello world!"

# your routes here


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
