from hashlib import sha256
from typing import Dict, Union

from apis import model


def enter_user(doc: Dict[str, Union[str, int]]):
    model.check_existing(doc)
    doc["password"] = sha256(doc["password"].encode()).hexdigest()
    model.register_user(doc)


def insert_data(unit_id: str, data: Dict[str, Union[str, int]]):
    model.insert_data(unit_id=unit_id, data=data)
