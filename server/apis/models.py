import os
import random
import string
from typing import Dict, Union

import pymongo
from core.errorfactory import (
    DuplicationError, ExcessiveUnitsError, InvalidCredentialsError
)


class Model:
    def __init__(self, *args, **kwargs):
        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        if os.getenv("DEBUG") or os.getenv("CI"):
            self.db = client[os.getenv("TESTDB")]
        else:
            self.db = client[os.getenv("DB")]

    def register_school(self, doc: Dict[str, Union[str, int]], limit: int = 50):
        """Register new schools and assign units

        Args:
            doc (Dict[str, Union[str, int]]): school data
        """

        _units = doc.get("units")
        if _units > limit:
            raise ExcessiveUnitsError("Unit limit excede")

        doc = {**{"unit_id": self.get_uid()}, **doc}
        self.db.schools.insert_one(doc)
        self.db.units.insert_one({"unit_id": doc["unit"]})

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