import json
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
    headers = {"Content-Type": "application/json"}

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

    def user_login(self, get_refresh=False):
        user_doc = self.user_register()
        response = self.request.post(
            self.base_url + "register", data=json.dumps(user_doc), headers=self.headers
        )
        self.assertEqual(response.status_code, 201)

        login_response = self.request.post(
            self.base_url + "auth/login",
            data=json.dumps(
                {"email": user_doc["email"], "password": user_doc["password"]}
            ),
            headers=self.headers,
        )
        self.assertEqual(login_response.status_code, 200)
        user_creds = login_response.json()
        if get_refresh:
            return user_creds
        return user_creds["access_token"]

    def clear_all(self):
        self.db.drop_collection("users")
        self.db.drop_collection("units")
        self.db.drop_collection("Admin")
        self.db.drop_collection("AdminCredentials")
