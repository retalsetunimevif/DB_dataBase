import argparse

from psycopg2 import connect, ProgrammingError

from clcrypto import check_password
from models import Message
from models import User


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--to", help="recipent name")
parser.add_argument("-s", "--send", help="message to send (maximum 255 characters)")
parser.add_argument("-l", "--list", help="list of messages", action="store_true")
args = parser.parse_args()


with open("db_connect") as file:
    user, host, password = file.readlines()

USER = user.strip()
PASS = password.strip()
HOST = host.strip()
DB = "users_db"


def print_messages(messages):
    for message in messages:
        print(f"{message.id} | {message.to_id} | {message.text}")

def show_messages(cnx, username, password):
    user = User.load_user_by_username(cnx.cursor(), username)
    if not user:
        print("User does not exists!")
    elif check_password(password, user.hashed_password):
        messages = Message.load_all_messages(cnx.cursor(), user.id)
        for message in messages:
            from_user = User.load_user_by_id(cnx.cursor(), message.from_id)
            print("~"*60)
            print(f"FROM: {from_user.username}")
            print(f"Data: {message.creation_date}")
            print("Message:\n", message.text)
            print("~"*60 +"\n")
    else:
        print("Incorrect password!")

def send_message(curosr, from_username, password, to_username, message):
    if len(message) > 255:
        print("Message is to long: maximum is 255 characters.")
        return None
    from_user = User.load_user_by_username(curosr.cursor(), from_username)
    if from_user and check_password(password, from_user.hashed_password):
        to_user = User.load_user_by_username(curosr.cursor(), to_username)
        if to_user:
            mess = Message(from_user.id, to_user.id, message)
            mess.save_to_db(curosr.cursor())
            print("Message send")
        else:
            print("Recipient does not exists")
    else:
        print("Incorrect password or Sender does not exists!")


def connect_to_DB(user=USER, password=PASS, host=HOST, db=DB):
    try:
        cnx = connect(user=user, password=password, host=host, database=db)
        cnx.autocommit = True
        if args.username and args.password and args.to and args.send:
            send_message(cnx, args.username, args.password, args.to, args.send)
        elif args.username and args.password and args.list:
            show_messages(cnx, args.username, args.password)
        else:
            parser.print_help()
    except ProgrammingError as PE:
        print(PE)
    else:
        cnx.close()


if __name__ == "__main__":
    connect_to_DB(USER, PASS, HOST, DB)
