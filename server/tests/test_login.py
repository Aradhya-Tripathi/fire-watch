from unittest import TestCase
import requests
from .base import user_register, clear_all
import json


class TestServer(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Start server
        """
        cls.request = requests.Session()
        cls.base_url = "http://localhost:8000/"

    def test_server(self):
        status = self.request.get(self.base_url + "apis/healthcheck")
        self.assertEqual(200, status.status_code)

    def test_register(self):
        clear_all()

        doc = user_register()
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

        doc = user_register()
        doc.pop("user_name")
        status = self.request.post(
            self.base_url + "apis/register", data=json.dumps(doc), headers=headers
        )
        self.assertEqual(status.status_code, 400)

    def test_login(self):
        clear_all()
        doc = user_register()
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
        self.assertIsInstance(status.json()["access_token"], str)
        self.assertIsInstance(status.json()["refresh_token"], str)
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
        clear_all()
