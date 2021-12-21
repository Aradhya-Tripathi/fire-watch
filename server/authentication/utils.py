from hashlib import sha256
from typing import Dict, Union

from fire_watch.errorfactory import InvalidToken

from authentication import auth_model


def get_token(headers: Dict[str, Union[int, str]]):
    try:
        token_type, token = headers["Authorization"].split()
        assert token_type == "Bearer"
    except Exception:
        raise InvalidToken(detail={"error": "Invalid token type"})
    return token


def validate_unit_id(token: str):
    return auth_model.validate_unit_id(unit_id=token)


def login(password: str, email: str):
    password = sha256(password.encode()).hexdigest()
    return auth_model.login(password, email)


def reset_password(data: Dict[str, str]) -> None:
    old_passwd = sha256(data["old_passwd"].encode()).hexdigest()
    new_passwd = sha256(data["new_passwd"].encode()).hexdigest()
    auth_model.reset_password(
        email_id=data["email_id"], old_passwd=old_passwd, new_passwd=new_passwd
    )


def admin_login(password: str, email: str):
    password = sha256(password.encode()).hexdigest()
    return auth_model.admin_login(password, email)
