import pymongo
from unittest import TestCase
import requests
from .base import school_register, DATABASE
import json


class TestUnit(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.request = requests.Session()
        cls.base_url = "http://localhost:8000/"
        cls.client = pymongo.MongoClient(DATABASE["Test"]["MONGO_URI"])
        cls.db = cls.client[DATABASE["Test"]["DB"]]

    def clear_all(self):
        self.db.drop_collection("schools")
        self.db.drop_collection("units")

    def register_school(self):
        headers = {"Content-Type": "application/json"}
        status = self.request.post(
            self.base_url + "apis/register",
            data=json.dumps(school_register()),
            headers=headers,
        )
        self.assertEqual(status.status_code, 201)

    def test_upload_route(self):
        self.register_school()

        school = self.db.schools.find_one(
            {"school_name": school_register()["school_name"]}
        )
        unit_id = school["unit_id"]

        headers = {
            "Authorization": f"Bearer {unit_id}",
            "Content-Type": "application/json",
        }
        status = self.request.post(self.base_url + "apis/upload", headers=headers)
        self.assertEqual(status.status_code, 201)

    def test_forbidden_upload(self):
        unit_id = "random"

        headers = {
            "Authorization": f"Bearer {unit_id}",
            "Content-Type": "application/json",
        }
        status = self.request.post(self.base_url + "apis/upload", headers=headers)
        self.assertEqual(status.status_code, 403)

    def setUp(self):
        self.clear_all()

    def tearDown(self):
        self.clear_all()
