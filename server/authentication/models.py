import pymongo
from core.errorfactory import InvalidUid
import os


class AuthModel:
    def __init__(self, *args, **kwargs):
        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        if os.getenv("DEBUG") or os.getenv("CI"):
            self.db = client[os.getenv("TESTDB")]
        else:
            self.db = client[os.getenv("DB")]

    def validate_request(self, unit_id: str):
        documents = self.db.units.count_documents({"unit_id": unit_id})
        if documents:
            return True
        raise InvalidUid(f"No document with unit with Id {unit_id} found")