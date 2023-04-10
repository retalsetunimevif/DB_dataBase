from psycopg2 import connect, OperationalError, ProgrammingError
from psycopg2.errors import DuplicateDatabase, DuplicateTable



with open("db_connect") as file:
    connection = [line.strip() for line in file.readlines()]

USER = connection[0]  # "user_name"
HOST = connection[1]  # "host_name_"
PASSWORD = connection[2]  # "password"
DB = "users_db"

SQL_CREATE_DB = f"CREATE DATABASE {DB};"
SQL_CREATE_TABLE_USERS = """
    CREATE Table users
        (
        id serial,
        username varchar(255),
        hashed_password varchar(80),
        PRIMARY KEY (id)
        );"""
SQL_CREATE_TABLE_MESSAGES = """
    CREATE TABLE messages
    (
    id serial,
    from_id int,
    to_id int,
    creation_date DATE,
    text varchar(255),
    PRIMARY KEY (id),
    FOREIGN KEY (from_id) REFERENCES users(id),
    FOREIGN KEY (to_id) REFERENCES  users(id)
    );
    """

try:
    cnx = connect(user=USER, password=PASSWORD, host=HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()
    print("połączono.")
    print(SQL_CREATE_DB)
    cursor.execute(sql)
    print('Zrobione')
except DuplicateDatabase as e:
    print(f'The DB: \"{DB}\" Exists!\n {e}')
except OperationalError:
    print("Nie połączono.")
else:
    cnx.close()

try:
    cnx = connect(user=USER, password=PASSWORD, host=HOST, database=DB)
    cursor = cnx.cursor()
    print("połączono.")
    cursor.execute(SQL_CREATE_TABLE_USERS)
    cnx.commit()
except DuplicateTable:
    print("The Table \"users\" are exists!")
except OperationalError:
    print("connection lost!.")
else:
    cnx.close()

try:
    cnx = connect(user=USER, password=PASSWORD, host=HOST, database=DB)
    cursor = cnx.cursor()
    print("przystępuję do tworzenia tabeli \"messges\".")
    cursor.execute(SQL_CREATE_TABLE_MESSAGES)
    cnx.commit()
    print("Table created.")
except DuplicateTable as DT:
    print(f'Table: "messages" already exists!\n{DT} ')
except OperationalError:
    print("Connection lost!")
except ProgrammingError:
    print("Query returns nothing.")
else:
    cnx.close()
