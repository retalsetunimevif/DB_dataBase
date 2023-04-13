import argparse

from psycopg2 import connect, ProgrammingError

from models import User


class UniqueViolation(Exception):
    pass


with open("db_connect") as file:
    user, host, password = file.readlines()


USER = user.strip()
PASS = password.strip()
HOST = host.strip()
DB = "users_db"

def connect_to_DB(func, user=USER, password=PASS, host=HOST, db=DB):
    try:
        cnx = connect(user=user, password=password, host=host, database=db)
        cnx.autocommit = True
        result = func(cnx.cursor())
    except ProgrammingError as PE:
        print(PE)
    else:
        cnx.close()
    return result

def list_of_users(cursor):
    users = User.load_all_users(cursor)
    return users

def create_user_and_save_to_db(username, password, salt=''):
    user = User(username, password, salt)
    result = connect_to_DB(user.save_to_db)


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="user password - minimum is 8 characters")
parser.add_argument("-n", "--new_pass", help="new password for user")
parser.add_argument("-l", "--list", help="list of users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
args = parser.parse_args()

if args.username and args.password:
    all_users = connect_to_DB(list_of_users)
    print(args.username, args.password)
    for user in all_users:
        if args.username == user.username:
            raise UniqueViolation("Such a user already exists!")
    else:
        if len(args.password) >= 8:
            print("hasło spełnia wymogi.")
            create_user_and_save_to_db(args.username, args.password)
        else:
            print("hasło jest za krótkie.")


