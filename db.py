import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Venmo (Full) app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        #connecting databse to program
        self.conn = sqlite3.connect(
             "todo.db", check_same_thread=False
        )
        # self.conn = sqlite3.connect(
        #     "app.db", check_same_thread=False
        # )
    
        self.delete_transactions_table()
        self.create_transactions_table()

        self.delete_users_table()
        self.create_users_table()
      

        

#----------------------------TRANSACTIONS---------------------------------------
    def create_transactions_table(self):
        """
        Using SQL, create transaction table
        """

        try:
            self.conn.execute(
                """
                CREATE TABLE transactions(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    accepted INTEGER
                );"""
            )
        except Exception as e:
            print(e)

    def delete_transactions_table(self):
        """
        Using SQL, deletes a transaction table
        """
        self.conn.execute("DROP TABLE IF EXISTS transactions;")

    def get_transactions_by_id(self, user_id):
        """
        Using SQL, gets all the transactions involving a user
        """
        users = self.conn.execute("SELECT * FROM transactions WHERE sender_id = ? OR receiver_id = ?;", (user_id, user_id))
        transactions = []
        for row in users:
            transactions.append({"id": row[0], "timestamp": row[1], "sender_id": row[2], "receiver_id": row[3], "amount": row[4], "accepted": row[5]})
        return transactions
    
    def delete_transactions_by_id(self, user_id):
        """
        Using SQL, deletes all the transactions including the user
        """
        user = self.conn.execute("DELETE FROM transactions WHERE sender_id=? OR receiver_id=?;", (user_id, user_id))
        self.conn.commit()
        for row in user: 
             return {"id": row[0], "name": row[1], "username": row[2], "balance": row[3]}
        return None
        
# ----------------------------USERS---------------------------------------------
    def create_users_table(self):
        """
        Using SQL, create user table
        """
        
        try:
            self.conn.execute(
                """
                CREATE TABLE users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    balance INTEGER NOT NULL
                );
                """
            )
        except Exception as e:
            print(e)

    def delete_users_table(self):
        """
        Using SQL, deletes a users table
        """
        self.conn.execute("DROP TABLE IF EXISTS users;")

    def get_all_users(self):
        """
        Using SQL, gets all users - does not return ID nor transactions
        """
        cursor = self.conn.execute("SELECT * FROM users;")
        users = []

        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username:": row[2]})

        return users
    
    def get_user_by_id(self, user_id):
         """
         Using SQL, gets a user
         """
         user = self.conn.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
         for row in user: 
             return {"id": row[0], "name": row[1], "username": row[2], "balance": row[3]}
         
         return None

    def create_user(self, name, username, balance):
        """
        Using SQL, creates user, and returns everything about the user
        """
        if not balance:
            c = self.conn.execute("""
            INSERT INTO users (name, username, balance)
            VALUES (?, ?, 0);
            """, (name, username))
            
        else:
            print("reached here 2")
            c = self.conn.execute("""
            INSERT INTO users (name, username, balance)
            VALUES (?, ?, ?);
            """, (name, username, balance))

        self.conn.commit()
        #returns the id of the user that was inserted
        return c.lastrowid
        
            
    def delete_user_by_id(self, user_id):
        """
        Using SQL, deletes a user
        """    
        user = self.conn.execute("DELETE FROM users WHERE id = ?;", (user_id,))
        self.conn.commit()
        for row in user: 
             return {"id": row[0], "name": row[1], "username": row[2], "balance": row[3]}
         

    def send_money(self, sender_id, receiver_id, amount):
        """
        Using SQL, sends money from one user to another
        """
        sender_bal = self.conn.execute("SELECT balance FROM users WHERE id=?;", (sender_id)) 
        if sender_bal < amount:
            return None
        sender_bal = sender_bal - amount


# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)