from .base import CustomTestCase
import json


class TestAuthentication(CustomTestCase):
    def setUp(self) -> None:
        self.clear_all()

    def test_register(self):
        doc = self.user_register()
        headers = {"Content-type": "application/json"}
        doc["units"] = 51
        status = self.request.post(
            self.base_url + "apis/register", data=json.dumps(doc), headers=headers
        )
        self.assertEqual(status.status_code, 400)
        doc = self.user_register()
        doc.pop("user_name")
        status = self.request.post(
            self.base_url + "apis/register", data=json.dumps(doc), headers=headers
        )
        self.assertEqual(status.status_code, 400)

    def test_login(self):
        doc = self.user_register()
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
        self.assertEqual(status.status_code, 401)

        creds = {"password": doc["password"], "email": "incorrect email"}
        status = self.request.post(
            self.base_url + "apis/login", data=json.dumps(creds), headers=headers
        )

        self.assertEqual(status.status_code, 401)

        creds = {"password": "incorrect password", "email": "incorrect email"}
        status = self.request.post(
            self.base_url + "apis/login", data=json.dumps(creds), headers=headers
        )

        self.assertEqual(status.status_code, 401)

    def test_protected_route(self):
        headers = {"Content-type": "application/json"}
        status = self.request.get(self.base_url + "apis/protected", headers=headers)
        self.assertEqual(status.status_code, 403)

        headers.update({"Authorization": "Bearer Ransodasodmasd"})
        status = self.request.get(self.base_url + "apis/protected", headers=headers)
        self.assertEqual(status.status_code, 403)

        doc = self.user_register()
        headers = {"Content-type": "application/json"}
        status = self.request.post(
            self.base_url + "apis/register", data=json.dumps(doc), headers=headers
        )
        self.assertEqual(status.status_code, 201)

        creds = {"password": doc["password"], "email": doc["email"]}
        tokens = self.request.post(
            self.base_url + "apis/login", data=json.dumps(creds), headers=headers
        )
        headers.update({"Authorization": f"Bearer {tokens.json()['access_token']}"})
        status = self.request.get(self.base_url + "apis/protected", headers=headers)
        self.assertEqual(status.status_code, 200)

    def tearDown(self) -> None:
        self.clear_all()
