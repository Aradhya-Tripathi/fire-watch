import os
import random
import string
from typing import Dict, Union
from core.settings import CONF

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
        if os.getenv("DEBUG") or os.getenv("CI"):
            self.db = client[os.getenv("TESTDB")]
        else:
            self.db = client[os.getenv("DB")]
        self.max_entry = CONF["max_unit_entry"]

    def register_school(self, doc: Dict[str, Union[str, int]], limit: int = 50):
        """Register new schools and assign units

        Args:
            doc (Dict[str, Union[str, int]]): school data
        """

        _units = doc.get("units")
        if _units > limit:
            raise ExcessiveUnitsError

        doc = {**{"unit_id": self.get_uid(length=16)}, **doc}
        self.db.schools.insert_one(doc)
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
        """Check existing schools

        Args:
            doc (Dict[str, Union[str, int]]): school data

        Raises:
            DuplicationError: If school exists
        """
        school = self.db.schools.find_one(
            {
                "$or": [
                    {"email": doc.get("email")},
                    {"school_name": doc.get("school_name")},
                ]
            }
        )
        if school:
            raise DuplicationError("School Exists")

    def credetials(self, password: str, email: str):
        school = self.db.schools.find_one({"password": password, "email": email})
        if school:
            return school
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
