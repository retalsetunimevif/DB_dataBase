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


def create_databse(sql_query, U, P, H):
    """
    :param sql_query: Query for createing databse:
    - example: "CREATE DATABASE cars_db;"
    :param U: User
    :param P: Password
    :param H: Host
    :return: return "True" if connected to the database and a query is performed
    """
    result = None
    try:
        cnx = connect(user=U, password=P, host=H)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql_query)
        result = True
    except DuplicateDatabase as e:
        print(f'The database already Exists!\n {e}')
    except OperationalError:
        print("connection lost!.")
    else:
        cnx.close()
    return result


def create_table(sql_query, U, P, H, DB):
    """
    :param sql_query: Query for createing table
    :param U: User
    :param P: Password
    :param H: Host
    :param DB: name of Database to connect
    :return: return "True" if connected to the database and a query is performed
    """
    result = None
    try:
        cnx = connect(user=U, password=P, host=H, database=DB)
        cursor = cnx.cursor()
        cursor.execute(sql_query)
        cnx.commit()
        result = True
    except DuplicateTable as DT:
        print(f"The table already exists!\n{DT}")
    except OperationalError:
        print("connection lost!.")
    else:
        cnx.close()
    return result


print(create_databse(SQL_CREATE_DB, USER, PASSWORD, HOST))
print(create_table(SQL_CREATE_TABLE_USERS, USER, PASSWORD, HOST, DB))
print(create_table(SQL_CREATE_TABLE_MESSAGES, USER, PASSWORD, HOST, DB))


