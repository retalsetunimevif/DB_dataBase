from psycopg2 import connect, OperationalError, ProgrammingError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

with open("db_connect") as file:
    connection = [line.strip() for line in file.readlines()]

USER = connection[0]  # "user_name"
HOST = connection[1]  # "host_name_"
PASSWORD = connection[2]  # "password"
DB = "users_db"

try:
    cnx = connect(user=USER, password=PASSWORD, host=HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()
    print("połączono.")
    sql = f"CREATE DATABASE {DB};"
    print(sql)
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
    sql = """
    CREATE Table users
        (
        id serial,
        username varchar(255),
        hashed_password varchar(80),
        PRIMARY KEY (id)
        );"""
    cursor.execute(sql)
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
    sql = """
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
    cursor.execute(sql)
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
