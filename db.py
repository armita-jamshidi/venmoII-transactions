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
             "users.db", check_same_thread=False
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
                    reciever_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    accepted INTEGER
                )"""
            )
        except Exception as e:
            print(e)

    def delete_transactions_table(self):
        """
        Using SQL, deletes a transaction table
        """
        self.conn.execute("DROP TABLE IF EXISTS transactions;")

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
                    transactions FOREIGN KEY (transaction_id) REFERENCES transactions
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

    def create_user(self, name, username, balance):
        """
        Using SQL, creates user, and returns everything about the user
        """
        if not balance:
            print("reached here")
            c = self.conn.execute("""
            INSERT INTO users (name, username, balance, transactions)
            VALUES (?, ?, 0, []);
            """, (name, username))
            
        else:
            print("reached here 2")
            c = self.conn.execute("""
            INSERT INTO users (name, username, balance, transactions)
            VALUES (?, ?, ?, []);
            """, (name, username, balance))

        self.conn.commit()
        #returns the id of the user that was inserted
        return c.lastrowid
        

    def get_user_by_id(self, user_id):
         """
         Using SQL, gets a user
         """
         user = self.conn.execute("SELECT * FROM users WHERE ID = ?", (user_id,))
         for row in user: 
             return {"id": row[0], "name": row[1], "username": row[2], "balance": row[3], "transactions": row[4]}
         
         return None
            
             

# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)