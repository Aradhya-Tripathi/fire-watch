import pymongo
from unittest import TestCase
import requests
from .base import user_register, DATABASE
import json
from core.settings import conf

from typing import Union, Dict


class TestUnit(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.request = requests.Session()
        cls.base_url = "http://localhost:8000/"
        cls.client = pymongo.MongoClient(DATABASE["Test"]["MONGO_URI"])
        cls.db = cls.client[DATABASE["Test"]["DB"]]

    def clear_all(self):
        self.db.drop_collection("users")
        self.db.drop_collection("units")

    def register_user(self, doc: Dict[str, Union[str, int]]):
        headers = {"Content-Type": "application/json"}
        status = self.request.post(
            self.base_url + "apis/register",
            data=json.dumps(doc),
            headers=headers,
        )
        return status

    def test_upload_route(self):
        self.register_user(user_register())

        user = self.db.users.find_one({"user_name": user_register()["user_name"]})
        unit_id = user["unit_id"]

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

    def test_excessive_units(self):
        doc = user_register(units=conf["max_unit_entry"] + 1)
        status = self.register_user(doc)
        self.assertEqual(status.status_code, 400)

    def setUp(self):
        self.clear_all()

    def tearDown(self):
        self.clear_all()
