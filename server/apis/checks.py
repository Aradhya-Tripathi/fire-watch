from core.errorfactory import (
    DuplicationError,
    ExcessiveUnitsError,
    InvalidCredentialsError,
    InvalidUid,
)
from typing import Dict, Union
from apis import model
from hashlib import sha256


def enter_user(doc: Dict[str, Union[str, int]]):
    try:
        model.check_existing(doc)
    except DuplicationError as e:
        return e

    try:
        doc["password"] = sha256(doc["password"].encode()).hexdigest()
        model.register_user(doc)
    except ExcessiveUnitsError as e:
        return e

    return None


def login(password: str, email: str):
    try:
        password = sha256(password.encode()).hexdigest()
        return model.credetials(password, email)
    except InvalidCredentialsError as e:
        return str(e)


def insert_data(unit_id: str, data: Dict[str, Union[str, int]]):
    try:
        return model.insert_data(unit_id=unit_id, data=data)
    except InvalidUid:
        return None


def reset_password(data: Dict[str, str]) -> None:
    old_passwd = sha256(data["old_passwd"].encode()).hexdigest()
    new_passwd = sha256(data["new_passwd"].encode()).hexdigest()
    model.reset_password(
        email_id=data["email_id"], old_passwd=old_passwd, new_passwd=new_passwd
    )
    return None
