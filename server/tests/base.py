import os
from unittest import TestCase

import pymongo
import requests
from dotenv import load_dotenv

load_dotenv()


DATABASE = {
    "Production": {
        "MONGO_URI": os.getenv("MONGO_URI"),
        "DB": os.getenv("DB"),
    },
    "Test": {"MONGO_URI": os.getenv("MONGO_URI"), "DB": os.getenv("TESTDB")},
}


class CustomTestCase(TestCase):
    request = requests.Session()
    base_url = "http://localhost:8000/"
    client = pymongo.MongoClient(DATABASE["Test"]["MONGO_URI"])
    db = client[DATABASE["Test"]["DB"]]

    def user_register(
        self,
        user_name: str = "Test",
        email: str = "tester@example.com",
        password: str = "password",
        units: int = 10,
    ):
        doc = {
            "user_name": user_name,
            "email": email,
            "password": password,
            "units": units,
        }

        return doc

    def clear_all(self):
        self.db.drop_collection("users")
        self.db.drop_collection("units")
