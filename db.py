import os
import sqlite3
import datetime

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
    
        # self.delete_transactions_table()
        self.create_transactions_table()

        # self.delete_users_table()
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
         

    def record_transaction(self, sender_id, receiver_id, amount, message, accepted):
        """
        Records transaction information in database
        """
        # time = datetime.now()
        time = "4pm"

        #below code returns the id of the most recent add
        t = self.conn.execute("INSERT INTO transactions (timestamp, sender_id, receiver_id, amount, accepted) VALUES (?, ?, ?, ?, ?);", 
                          (time, sender_id, receiver_id, amount, accepted))
        self.conn.commit()

        #t.lastrowid is the id of the most recently added row
        return ({"id": t.lastrowid, "timestamp": time, "sender_id": sender_id, "receiver_id": receiver_id, "amount":amount, "message": message, "accepted": accepted})
        
    
    def send_money(self, sender_id, receiver_id, amount, message, accepted):
        """
        Using SQL, sends money from one user to another
        """
        sender = self.conn.execute("SELECT * FROM users WHERE id=?;", (sender_id,))
        for row in sender: 
            sender_bal = row[3]
        receiver = self.conn.execute("SELECT * FROM users WHERE id=?;", (receiver_id,)) 
        for row in receiver:
            receiver_bal = receiver[3]

        if sender_bal < amount:
            return None
        sender_bal = sender_bal - amount
        receiver_bal = receiver_bal + amount

        self.conn.execute("UPDATE users SET balance = ? WHERE id = ?;", (receiver_bal, receiver_id))
        self.conn.execute("UPDATE users SET balance = ? WHERE id = ?;", (sender_bal, sender_id))
        
        self.conn.commit()
        #return 1 if send_money was successful - need to call record_transaction for final answer
        return 1



# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)