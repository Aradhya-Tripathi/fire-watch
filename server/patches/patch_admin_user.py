import getpass
import re
import sys
from hashlib import sha256

import fire_watch
from django.core.management import execute_from_command_line


email_re = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def create_admin_user():
    email = input("Email: ")
    password = getpass.getpass("Password: ")

    if not email_re.fullmatch(email) or not password:
        fire_watch.print("[bold red]Enter valid details!")
        sys.exit(0)

    if admin := fire_watch.db.AdminCredentials.find_one({"email": email}):
        fire_watch.print(f"[bold red]Admin: {admin['email']} already exists!")
        sys.exit(0)

    password = sha256(password.encode()).hexdigest()
    fire_watch.db.AdminCredentials.insert_one({"email": email, "password": password})
    fire_watch.print(f"[bold green]Added new admin {email}!")


def remove_admin_user():
    email = input("Email: ")
    password = getpass.getpass("Password: ")

    if not password or not email_re.fullmatch(email):
        fire_watch.print("[bold red]Please enter valid details!")
        sys.exit(0)

    password = sha256(password.encode()).hexdigest()
    admin = fire_watch.db.AdminCredentials.find_one(
        {"email": email, "password": password}
    )
    if not admin:
        fire_watch.print("[bold red]Invalid credentials!")
        sys.exit(0)
    fire_watch.db.AdminCredentials.find_one_and_delete({"email": email})
    fire_watch.print(f"[bold green]Removed admin {admin['email']}!")


def list_admins():
    admins = list(fire_watch.db.AdminCredentials.find({}, {"_id": 0, "password": 0}))
    if not admins:
        fire_watch.print("[bold red]No admins present!")
        sys.exit(0)
    fire_watch.print_json(data=admins)


def change_password():
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    new_password = getpass.getpass("New Password: ")

    if not password or not email_re.fullmatch(email) or not new_password:
        fire_watch.print("[bold red]Please enter valid details!")
        sys.exit(0)

    password = sha256(password.encode()).hexdigest()
    new_password = sha256(new_password.encode()).hexdigest()
    doc = fire_watch.db.AdminCredentials.find_one_and_update(
        {"email": email, "password": password},
        {"$set": {"password": new_password}},
    )
    if not doc:
        fire_watch.print("[bold red]Invalid Credentials!")
        sys.exit(0)
    fire_watch.print("[bold green]Updated password!")


def show_conf():
    fire_watch.print_json(data=fire_watch.conf)


print("\033[1mRunning Patches!")
execute_from_command_line.create_admin_user = create_admin_user
execute_from_command_line.remove_admin_user = remove_admin_user
execute_from_command_line.list_admins = list_admins
execute_from_command_line.show_conf = show_conf
execute_from_command_line.change_admin_password = change_password
