from typing import Dict, Union

from fire_watch.errorfactory import InvalidCredentialsError, InvalidUid

from .base_model import BaseModel
from admin import admin_model


class AuthModel(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_unit_id(self, unit_id: str):
        documents = self.db.units.find_one({"unit_id": unit_id})
        if documents:
            return True
        raise InvalidUid(
            f"No document with unit with Id {unit_id} found", status_code=401
        )

    def id_from_user(self, user_name: str):
        user = self.db.users.find_one({"user_name": user_name})
        return user["unit_id"]

    def register_user(self, doc: Dict[str, Union[str, int]]):
        """Register new users and assign units.

        Args:
            doc (Dict[str, Union[str, int]]): user data
        """

        units = doc.get("units")
        self.check_excessive_units(units)

        doc = {**{"unit_id": self.get_uid(length=16)}, **doc}
        self.db.users.insert_one(doc)
        self.db.units.insert_one({"unit_id": doc["unit_id"], "data": []})
        admin_model.log_user_request(
            {"unit_id": doc["unit_id"], "email": doc["email"], "units": doc["units"]}
        )

    def credentials(self, password, email):
        user = self.db.users.find_one({"password": password, "email": email})
        if user:
            return user
        raise InvalidCredentialsError(detail={"error": "Invalid credentials"})

    def reset_password(self, old_passwd: str, email_id: str, new_passwd: str):
        """Takes in hashed passwords updates
           password if user found.

        Args:
            old_pswd (str): old hashed password
            new_pswd (str): new hashed password
            email_id (str): email_id
        """
        self.db.users.find_one_and_update(
            {"password": old_passwd, "email": email_id},
            update={"$set": {"password": new_passwd}},
        )
        return None
