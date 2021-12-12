import os
import random
import string
from typing import Dict, Union

import pymongo
from free_watch import conf
from free_watch.errorfactory import (
    DuplicationError,
    InvalidUid,
)
from authentication import auth_model


class Model:
    def __init__(self, *args, **kwargs):
        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        if conf["developer"] or os.getenv("CI"):
            self.db = client[os.getenv("TESTDB")]
        else:
            self.db = client[os.getenv("DB")]
        self.max_entry = conf["max_unit_entry"]

    def register_user(self, **kwargs):
        auth_model.register_user(**kwargs)

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
            raise DuplicationError({"error": "User exists!"})

    def credetials(self, **kwargs):
        return auth_model.credentials(**kwargs)

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
        except IndexError:
            raise InvalidUid(detail={"error": f"No unit with the id {unit_id} found"})

        if len(unit["data"]) < self.max_entry:
            self.db.units.update_one(
                {"_id": unit["_id"]}, update={"$push": {"data": data}}
            )
        else:
            doc = {"unit_id": unit_id, "data": [data]}
            self.db.units.insert_one(doc)

    def reset_password(self, **kwargs) -> None:
        auth_model.reset_password(**kwargs)
