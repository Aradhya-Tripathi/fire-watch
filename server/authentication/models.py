import pymongo
import os
from free_watch import conf
from free_watch.errorfactory import InvalidUid


class AuthModel:
    def __init__(self, *args, **kwargs):
        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        if conf["developer"] or os.getenv("CI"):
            self.db = client[os.getenv("TESTDB")]
        else:
            self.db = client[os.getenv("DB")]

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
