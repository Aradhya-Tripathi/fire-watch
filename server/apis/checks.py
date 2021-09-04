from core.errorfactory import DuplicationError, ExcessiveUnitsError
from typing import Dict, Union
from apis import model
from hashlib import sha256


def enter_school(doc: Dict[str, Union[str, int]]):
    try:
        model.check_existing(doc)
    except DuplicationError as e:
        return e

    try:
        doc["password"] = sha256(doc["password"].encode()).hexdigest()
        model.register_school(doc)
    except ExcessiveUnitsError as e:
        return e

    return None