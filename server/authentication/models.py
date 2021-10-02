import pymongo
import os
from core.errorfactory import InvalidUid


class AuthModel:
    def __init__(self, *args, **kwargs):
        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        if os.getenv("DEBUG") or os.getenv("CI"):
            self.db = client[os.getenv("TESTDB")]
        else:
            self.db = client[os.getenv("DB")]

    def validate_token(self, unit_id: str):
        documents = self.db.units.find_one({"unit_id": unit_id})
        if documents:
            return True
        raise InvalidUid(f"No document with unit with Id {unit_id} found")

    def id_from_school(self, school_name: str):
        school = self.db.schools.find_one({"school_name": school_name})
        return school["unit_id"]
