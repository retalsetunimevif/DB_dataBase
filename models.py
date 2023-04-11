from psycopg2 import connect, ProgrammingError
from clcrypto import hash_password
import time


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
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                    VALUES (%s, %s) RETURNING id;
                    """
            cursor.execute(sql, (self.username, self._hashed_password))
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE users SET username=%s, hashed_password=%s
            WHERE id=%s
            """
            cursor.execute(sql, self.username, self.hashed_password, self.id)
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
            return True
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
        sql = "DELETE FROM user WHERE id=%s"
        cursor.execute(sql, (self._id, ))
        self._id = -1
        return True

class Message:
    def __init__(self, from_id, to_id, text, creation_date=None):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date

    @property
    def id(self):
        return self._id


    def save_to_db(self, cursor):
        if self._id = 1:
            sql = "INSERT INTO messages(from_id, to_id, text, creation_date)"
            VALUES(%s, %s, %s, %s)
            cursor.execute(sql, (self.from_id, self.to_id, self.text, time.strftime("%d-%m-%Y %H:%M:%S")))
            self._id = cursor.fetchone()[0]
            return True
        # else:
        #     sql = "UPDATE messages SET text=%s, cration_date=%s where id=%s and from_id=%s and to_id=%s;)
        #     cursor.execute(sql, ())
        return None

# u1 = User("marcin", "TestNr1")
# u3 = User("marcin", "testnr2")
# u5 = User("Cat", 'animalfood')
# # u1.hashed_password = "nowehaslo"
# # print(u1.hashed_password)
# try:
#     cnx = connect(user="postgres", password="coderslab", host="localhost", database="users_db")
#     cnx.autocommit = True
#     # u1.save_to_db(cnx.cursor())
#     # u3.save_to_db(cnx.cursor())
#     # u5.save_to_db(cnx.cursor())
#     u2 = User.load_user_by_username(cnx.cursor(), "marcin")
#     u4 = User.load_user_by_id(cnx.cursor(), 2)
#     all_users = User.load_all_users(cnx.cursor())
#     users_the_same_name = User.load_users_by_username(cnx.cursor(), "marcin")
# except ProgrammingError as PE:
#     print(PE)
# else:
#     cnx.close()
# print(u2.id, u2.username, u2.hashed_password)
# print(u4.id, u4.username, u4.hashed_password)
# print(all_users[0].username, all_users[1].id)
# for user in all_users:
#     print(user.id, "|", user.username, "|", user.hashed_password)
#
# print(users_the_same_name)
# for user in users_the_same_name:
#     print(user.id, user.username,user.hashed_password)
