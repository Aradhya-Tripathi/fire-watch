import os
import secrets
from datetime import datetime, timedelta
from typing import Dict, Union

import fire_watch
import jwt


class TokenAuth:
    def __init__(self):
        self.signature = (
            os.getenv("SECRET_KEY")
            if fire_watch.flags.use_secret
            else secrets.token_hex()
        )

    @staticmethod
    def set_expiry(payload: Dict[str, str], current_time, time):
        if isinstance(time, timedelta):
            payload["exp"] = current_time + time
        else:
            payload["exp"] = current_time + timedelta(hours=time)

    def generate_key(
        self,
        payload: Dict[str, Union[str, int]],
        expiry: Union[int, timedelta] = 1,
        get_refresh: bool = False,
        is_admin: bool = False,
        **kwargs,
    ):

        current_time = datetime.utcnow()
        self.set_expiry(payload, current_time, expiry)
        payload.update({"is_admin": True}) if is_admin else payload.update(
            {"is_admin": False}
        )
        access_token = jwt.encode(payload, key=self.signature)

        if get_refresh:
            if value := kwargs.get("refresh_exipry", expiry):
                self.set_expiry(payload, current_time, value)
            refresh_payload = {**{"refresh": True}, **payload}
            refresh_token = jwt.encode(refresh_payload, key=self.signature)
            return {"access_token": access_token, "refresh_token": refresh_token}

        return dict(access_token=access_token)

    def verify_key(self, is_admin: bool, key: Union[str, Dict[str, str]]):
        if isinstance(key, dict):
            key = key["access_token"]
        try:
            payload = jwt.decode(
                jwt=key.encode(),
                key=self.signature,
                options={"verify_exp": True, "verify_signature": True},
                algorithms=["HS256"],
            )
            assert (
                self.verify_role(is_admin, payload) == True
            ), "Role verification failed!"
        except Exception:
            return
        return payload

    def verify_role(self, is_admin, payload):
        return payload.get("is_admin") == is_admin
