from psycopg2 import connect, ProgrammingError
from clcrypto import hash_password


class User:
    pass
    def __init__(self, username, password='', salt=''):  # we can add second param:"salt"
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)  # we can add second param:"salt"

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
        return False

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
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
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_, ))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            load_user = User(username)
            load_user._id = id_
            load_user._hashed_password = hashed_password
            return load_user
        return None

u1 = User("marcin", "TestNr1")
u3 = User("marcin", "testnr2")
# u1.hashed_password = "nowehaslo"
# print(u1.hashed_password)
try:
    cnx = connect(user="postgres", password="coderslab", host="localhost", database="users_db")
    cnx.autocommit = True
    # u1.save_to_db(cnx.cursor())
    # u3.save_to_db(cnx.cursor())
    u2 = User.load_user_by_username(cnx.cursor(), "marcin")
    u4 = User.load_user_by_id(cnx.cursor(), 2)
except ProgrammingError as PE:
    print(PE)
else:
    cnx.close()
print(u2.id())
print(u2.username)
print(u2.hashed_password)
print(u4.id(), u4.username, u4.hashed_password)
