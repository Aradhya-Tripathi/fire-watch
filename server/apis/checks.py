from core.errorfactory import (
    DuplicationError,
    ExcessiveUnitsError,
    InvalidCredentialsError,
    InvalidUid,
)
from typing import Dict, Union
from apis import model
from hashlib import sha256
from core import conf


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
