from unittest import TestCase
import requests
from base import school_register
import json


class TestServer(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Start server
        """
        cls.request = requests.Session()
        cls.base_url = "http://localhost:8000/"

    def clear_all(self):
        import pymongo
        import os
        from dotenv import load_dotenv

        load_dotenv()

        client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        db = client[os.getenv("TESTDB")]

        db.drop_collection("schools")
        db.drop_collection("units")

    def test_server(self):
        status = self.request.get(self.base_url + "apis/healthcheck")
        self.assertEqual(200, status.status_code)

    def test_register(self):
        self.clear_all()

        doc = school_register()
        headers = {"Content-type": "application/json"}
        status = self.request.post(
            self.base_url + "apis/register", data=json.dumps(doc), headers=headers
        )
        self.assertEqual(status.status_code, 201)
        doc["units"] = 51
        status = self.request.post(
            self.base_url + "apis/register", data=json.dumps(doc), headers=headers
        )
        self.assertEqual(status.status_code, 400)

        doc = school_register()
        doc.pop("school_name")
        status = self.request.post(
            self.base_url + "apis/register", data=json.dumps(doc), headers=headers
        )
        self.assertEqual(status.status_code, 400)

    def test_login(self):
        self.clear_all()
        doc = school_register()
        headers = {"Content-type": "application/json"}
        status = self.request.post(
            self.base_url + "apis/register", data=json.dumps(doc), headers=headers
        )
        self.assertEqual(status.status_code, 201)

        creds = {"password": doc["password"], "email": doc["email"]}
        status = self.request.post(
            self.base_url + "apis/login", data=json.dumps(creds), headers=headers
        )

        self.assertEqual(status.status_code, 200)
        creds = {"password": "incorrectpassword", "email": doc["email"]}
        status = self.request.post(
            self.base_url + "apis/login", data=json.dumps(creds), headers=headers
        )
        self.assertEqual(status.status_code, 403)

        creds = {"password": doc["password"], "email": "incorrect email"}
        status = self.request.post(
            self.base_url + "apis/login", data=json.dumps(creds), headers=headers
        )

        self.assertEqual(status.status_code, 403)

        creds = {"password": "incorrect password", "email": "incorrect email"}
        status = self.request.post(
            self.base_url + "apis/login", data=json.dumps(creds), headers=headers
        )

        self.assertEqual(status.status_code, 403)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.clear_all(cls)
