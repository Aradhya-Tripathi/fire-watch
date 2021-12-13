import os
import random
import string

import pymongo

from . import conf


class BaseModel:
    def __init__(self, *args, **kwargs):
        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = (
            client[os.getenv("TESTDB")]
            if conf["developer"] or os.getenv("CI")
            else client[os.getenv("DB")]
        )
        self.max_entry = conf["max_unit_entry"]

    def get_uid(self, length: int):
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
