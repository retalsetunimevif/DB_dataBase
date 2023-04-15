import argparse

from psycopg2 import connect, ProgrammingError
from psycopg2.errors import UniqueViolation

from clcrypto import check_password
from models import User


with open("db_connect") as file:
    user, host, password = file.readlines()


USER = user.strip()
PASS = password.strip()
HOST = host.strip()
DB = "users_db"

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="user password - minimum is 8 characters")
parser.add_argument("-n", "--new_pass", help="new password for user")
parser.add_argument("-l", "--list", help="list of users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
args = parser.parse_args()


def load_user(cursor, username):
    return User.load_user_by_username(cursor, username)


def create_user(cnx, username, password):
    if len(password) >= 8:
        try:
            user = User(username, password)
            user.save_to_db(cnx.cursor())
            print("Done: User created.")
        except UniqueViolation:
            print("User alerady exists!")
    else:
        print("Password is to short!")

def del_user(cnx, username, password):
    user = load_user(cnx.cursor(), username)
    if user:
        if check_password(password, user.hashed_password):
            user.delete_user(cnx.cursor())
            print("User deleted.")
        else:
            print("Incorrect password.")
    else:
        print(f"User does not exit: \"{args.username}\".")

def edit_user(cnx, username, password, new_pass):
    user = User.load_user_by_username(cnx.cursor(), username)
    if user:
        if check_password(password, user.hashed_password):
            if len(password) >= 8:
                user.hashed_password = new_pass
                user.save_to_db(cnx.cursor())
                print("Password changed.")
            else:
                print("Password is to short")
        else:
            print("Incorrect password!")
    else:
        print("User does not exit!")

def list_of_users(cursor):
    return User.load_all_users(cursor)

def print_all_users(users):
    print("ID| USERNAME")
    for user in users:
        print(user.id, '|', user.username)

def connect_to_DB(user=USER, password=PASS, host=HOST, db=DB):
    try:
        cnx = connect(user=user, password=password, host=host, database=db)
        cnx.autocommit = True
        users = list_of_users(cnx.cursor())
        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cnx, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            del_user(cnx, args.username, args.password)
        elif args.username and args.password:
            create_user(cnx, args.username, args.password)
        elif args.list:
            print_all_users(users)
        else:
            print("help")
            print(args.print_help())
    except ProgrammingError as PE:
        print(PE)
    else:
        cnx.close()


if __name__ == "__main__":
    connect_to_DB(USER, PASS, HOST, DB)
