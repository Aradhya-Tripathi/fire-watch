import os
import random
import string
from typing import Dict, Union

from pymongo.message import update
from core import conf

import pymongo
from core.errorfactory import (
    DuplicationError,
    ExcessiveUnitsError,
    InvalidCredentialsError,
    InvalidUid,
)


class Model:
    def __init__(self, *args, **kwargs):
        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        if conf["developer"] or os.getenv("CI"):
            self.db = client[os.getenv("TESTDB")]
        else:
            self.db = client[os.getenv("DB")]
        self.max_entry = conf["max_unit_entry"]

    def register_user(self, doc: Dict[str, Union[str, int]], limit: int = 50):
        """Register new users and assign units

        Args:
            doc (Dict[str, Union[str, int]]): user data
        """

        _units = doc.get("units")
        if _units > limit:
            raise ExcessiveUnitsError(units=_units)

        doc = {**{"unit_id": self.get_uid(length=16)}, **doc}
        self.db.users.insert_one(doc)
        self.db.units.insert_one({"unit_id": doc["unit_id"], "data": []})

    def get_uid(self, length: int = 8) -> str:
        """

        Args:
            length (int, optional): length of uuid. Defaults to 8.

        Returns:
            str: uuid
        """

        uid = random.choices(string.ascii_uppercase, k=length)
        if self.db.collection.find_one({"_id": uid}):
            return self.get_uid()
        return "".join(uid)

    def check_existing(self, doc: Dict[str, Union[str, int]]):
        """Check existing users

        Args:
            doc (Dict[str, Union[str, int]]): user data

        Raises:
            DuplicationError: If user exists
        """
        user = self.db.users.find_one(
            {
                "$or": [
                    {"email": doc["email"]},
                    {"user_name": doc["user_name"]},
                ]
            }
        )
        if user:
            raise DuplicationError("user Exists")

    def credetials(self, password: str, email: str):
        user = self.db.users.find_one({"password": password, "email": email})
        if user:
            return user
        raise InvalidCredentialsError("Invalid credentials")

    def insert_data(self, unit_id: str, data: Dict[str, Union[str, int]]):
        """Insert collected data into respective unit documents.
           Insert into document if current insertions are less than
           200 else create new unit document with same unit id and
           insert.

           Can be used as a standalone function to insert data or
           through available `upload` api route

        Args:
            unit_id (str): unique unit identifier
            data (Dict[str, Union[str, int]]): data collected

        Raises:
            InvalidUid: raised if no unit found
        """
        units = list(self.db.units.find({"unit_id": unit_id}))
        try:
            unit = units.pop()
        except IndexError as e:
            raise InvalidUid(f"No unit with the id {unit_id} found")

        if len(unit["data"]) < self.max_entry:
            self.db.units.update_one(
                {"_id": unit["_id"]}, update={"$push": {"data": data}}
            )
            return True

        doc = {"unit_id": unit_id, "data": [data]}
        self.db.units.insert_one(doc)
        return True

    def reset_password(self, email_id: str, old_passwd: str, new_passwd: str) -> None:
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
