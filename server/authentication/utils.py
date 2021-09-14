from typing import Union, Dict
from authentication import auth_model


def get_token(headers: Dict[str, Union[int, str]]):
    token_type, token = headers["Authorization"].split()
    assert token_type == "Bearer"
    return token


def validate_token(token: str):
    return auth_model.validate_request(unit_id=token)
