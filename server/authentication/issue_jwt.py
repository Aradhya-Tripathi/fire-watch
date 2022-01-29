import os
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Union

import fire_watch
import jwt


def set_expiry(payload: Dict[str, str], current_time, time):
    payload["exp"] = (
        current_time + time
        if isinstance(time, timedelta)
        else current_time + timedelta(hours=time)
    )


class Validator:
    def verify_key(
        self, key: Union[str, Dict[str, str]], is_admin: Optional[bool] = None
    ):
        if isinstance(key, dict):
            # Only verify access token by default if a dict is passed in.
            # Use is_valid_refresh to verify refresh token.
            key = key["access_token"]
        try:
            payload = jwt.decode(
                jwt=key.encode(),
                key=self.signature,
                options={"verify_exp": True, "verify_signature": True},
                algorithms=["HS256"],
            )
            if is_admin is not None:
                assert (
                    self.verify_role(is_admin, payload) is True
                ), "Role verification failed!"
        except Exception:
            return
        return payload

    def verify_role(self, is_admin, payload):
        return payload.get("is_admin") == is_admin


class AuthToken(Validator):
    def __init__(self):
        self.signature = (
            os.getenv("SECRET_KEY")
            if fire_watch.flags.use_secret
            else secrets.token_hex()
        )
        self.token_expiration = fire_watch.conf.token_expiration
        self.refresh_expiration = fire_watch.conf.refresh_expiration

    def generate_key(
        self,
        payload: Dict[str, Union[str, int]],
        expiry: Union[int, timedelta] = 1,
        get_refresh: bool = False,
        is_admin: bool = False,
        refresh_expiry: Union[int, timedelta] = 12,
    ):

        current_time = datetime.utcnow()
        set_expiry(payload, current_time, expiry)
        payload.update({"is_admin": True}) if is_admin else payload.update(
            {"is_admin": False}
        )
        access_token = jwt.encode(payload, key=self.signature)

        if get_refresh:
            set_expiry(payload, current_time, refresh_expiry)
            refresh_payload = {**{"refresh": True}, **payload}
            refresh_token = jwt.encode(refresh_payload, key=self.signature)
            return {"access_token": access_token, "refresh_token": refresh_token}

        return dict(access_token=access_token)

    def refresh_to_access(self, key):
        if payload := self.verify_key(is_admin=None, key=key):
            is_admin = payload["is_admin"]
            if payload.get("refresh"):
                del payload["refresh"]
                return self.generate_key(
                    payload=payload,
                    expiry=self.token_expiration,
                    get_refresh=True,
                    refresh_expiry=self.refresh_expiration,
                    is_admin=is_admin,
                )

    def is_valid_refresh(self, key):
        payload = self.verify_key(key)
        if payload:
            return payload.get("refresh", False)
        return False

    def valid_for(self, key: Union[str, int]):
        """Checks the `alive_for` time of a token.
        returns False if token already expired or invalid.

        Args:
            key Union[int, str]: token
        """
        current_time = datetime.utcnow()

        if isinstance(key, int):
            return datetime.utcfromtimestamp(key) - current_time

        if payload := self.verify_key(key):
            expiration = datetime.utcfromtimestamp(payload["exp"])
            return expiration - current_time
