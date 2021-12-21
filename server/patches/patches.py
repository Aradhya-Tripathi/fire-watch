import getpass
import os
import re
import sys
from hashlib import sha256

import fire_watch
import pymongo
from django.core.management import execute_from_command_line


def create_admin_user():
    email_re = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client[fire_watch.flags.db_name]
    email = input("Email: ")
    if not email_re.fullmatch(email):
        fire_watch.print("[bold red]Enter valid email!")
        sys.exit(0)
    password = getpass.getpass("Password: ")
    if password:
        password = sha256(password.encode()).hexdigest()
        db.AdminCredentials.insert_one({"email": email, "password": password})


print("\033[1mRunning Patches!")
execute_from_command_line.create_admin_user = create_admin_user
