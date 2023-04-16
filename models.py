from psycopg2 import connect, ProgrammingError
import time

from clcrypto import hash_password


# with open("db_connect") as file:
#     user, host, password = file.readlines()
#
#
# USER = user.strip()
# PASS = password.strip()
# HOST = host.strip()
# DB = "users_db"


class User:
    pass
    def __init__(self, username, password='', salt=''):  # we can add second param:"salt"
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)  # we can add second param:"salt"

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=''):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        return self.set_password(password)

    def save_to_db(self, cursor):
        if self.id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                    VALUES (%s, %s) RETURNING id;
                    """
            cursor.execute(sql, (self.username, self._hashed_password))
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE users SET username=%s, hashed_password=%s
                        WHERE id=%s;"""
            cursor.execute(sql, (self.username, self.hashed_password, self.id))
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s;"
        cursor.execute(sql, (username, ))
        data = cursor.fetchone()
        if data:
            id_, username, hash_password = data
            load_user = User(username)
            load_user._id = id_
            load_user._hashed_password = hash_password
            return load_user
        return None

    @staticmethod
    def load_users_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s;"
        cursor.execute(sql, (username,))
        users = []
        for row in cursor.fetchall():
            id_, username, hash_password = row
            load_user = User(username)
            load_user._id = id_
            load_user._hashed_password = hash_password
            users.append(load_user)
        return users


    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s;"
        cursor.execute(sql, (id_, ))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            load_user = User(username)
            load_user._id = id_
            load_user._hashed_password = hashed_password
            return load_user
        return None

    @staticmethod
    def load_all_users(cursor):
        users = []
        sql = "SELECT id, username, hashed_password FROM users;"
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            load_user = User(username)
            load_user._id = id_
            load_user._hashed_password = hashed_password
            users.append(load_user)
        return users

    def delete_user(self, cursor):
        print("deleting... ")
        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (self._id, ))
        self._id = -1
        return True

class Message:
    def __init__(self, from_id, to_id, text='', creation_date=None):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date

    @property
    def id(self):
        return self._id

    def set_message(self, text):
        self.text = text

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text, creation_date)
            VALUES(%s, %s, %s, %s) RETURNING id;"""
            cursor.execute(sql, (self.from_id, self.to_id, self.text, time.strftime("%d-%m-%Y %H:%M:%S")))
            self._id = cursor.fetchone()[0]
            return True
        # else:
        #     sql = "UPDATE messages SET text=%s, creation_date=%s WHERE id=%s;"
        #     cursor.execute(sql, (self.text, time.strftime("%d-%m-%Y %H:%M:%S"), self._id))
        #     return True
        return None

    @staticmethod
    def load_all_messages(cursor, user_id=None):
        messages = []
        if user_id:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages where to_id=%s;"
            cursor.execute(sql, (user_id, ))
        else:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages;"
            cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            load_message = Message(from_id, to_id)
            load_message._id = id_
            load_message.text = text
            load_message.creation_date = creation_date
            messages.append(load_message)
        return messages


# def connect_to_DB(user, password, host, db):
#     try:
#         cnx = connect(user=user, password=password, host=host, database=db)
#         cnx.autocommit = True
#
#
#     except ProgrammingError as PE:
#         print(PE)
#     else:
#         cnx.close()

if __name__ == "__main__":
    # connect_to_DB(USER, PASS, HOST, DB)
    pass
