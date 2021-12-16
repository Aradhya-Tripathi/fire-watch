import os
import secrets
from datetime import datetime, timedelta
from typing import Dict, Union

import jwt

import fire_watch

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
        **kwargs,
    ):

        current_time = datetime.utcnow()
        self.set_expiry(payload, current_time, expiry)

        access_token = jwt.encode(payload, key=self.signature)

        if get_refresh:
            if value := kwargs.get("refresh_exipry", expiry):
                self.set_expiry(payload, current_time, value)
            refresh_payload = {**{"refresh": True}, **payload}
            refresh_token = jwt.encode(refresh_payload, key=self.signature)
            return {"access_token": access_token, "refresh_token": refresh_token}

        return dict(access_token=access_token)

    def verify_key(self, key: Union[str, Dict[str, str]]):
        if isinstance(key, dict):
            key = key["access_token"]
        try:
            payload = jwt.decode(
                jwt=key.encode(),
                key=self.signature,
                options={"verify_exp": True, "verify_signature": True},
                algorithms=["HS256"],
            )
        except Exception:
            return
        return payload
