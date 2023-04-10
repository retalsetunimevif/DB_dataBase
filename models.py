from psycopg2 import connect, ProgrammingError
from clcrypto import hash_password


class User:
    pass
    def __init__(self, username, password, salt=''):  # we can add second param:"salt"
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
            sql = f"""INSERT INTO users(username, hashed_password)
                    VALUES (%s, %s) RETURNING id;
                    """
            cursor.execute(sql, (self.username, self._hashed_password))
            self._id = cursor.fetchone()[0]
            return True
        return False

u1 = User("marcin", "TestNr1")
u1.hashed_password = "nowehaslo"
print(u1.hashed_password)
try:
    cnx = connect(user="postgres", password="coderslab", host="localhost", database="users_db")
    cnx.autocommit = True
    u1.save_to_db(cnx.cursor())
except ProgrammingError as PE:
    print(PE)

else:
    cnx.close()
