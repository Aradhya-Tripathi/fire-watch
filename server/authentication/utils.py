from typing import Union, Dict
from authentication import auth_model
from core.errorfactory import InvalidToken


def get_token(headers: Dict[str, Union[int, str]]):
    try:
        token_type, token = headers["Authorization"].split()
        assert token_type == "Bearer"
    except (ValueError, AssertionError) as e:
        raise InvalidToken(detail={"error": "Invalid token type"})
    return token


def validate_unit_id(token: str):
    return auth_model.validate_unit_id(unit_id=token)
