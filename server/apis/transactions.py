from hashlib import sha256
from typing import Dict, Union

from apis import model


def enter_user(doc: Dict[str, Union[str, int]]):
    model.check_existing(doc)
    doc["password"] = sha256(doc["password"].encode()).hexdigest()
    model.register_user(doc)


def login(password: str, email: str):
    password = sha256(password.encode()).hexdigest()
    return model.credetials(password, email)


def insert_data(unit_id: str, data: Dict[str, Union[str, int]]):
    return model.insert_data(unit_id=unit_id, data=data)


def reset_password(data: Dict[str, str]) -> None:
    old_passwd = sha256(data["old_passwd"].encode()).hexdigest()
    new_passwd = sha256(data["new_passwd"].encode()).hexdigest()
    model.reset_password(
        email_id=data["email_id"], old_passwd=old_passwd, new_passwd=new_passwd
    )
