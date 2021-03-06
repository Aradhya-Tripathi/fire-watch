from .base import CustomTestCase
import json


ME = "user/me"


class TestAuthentication(CustomTestCase):
    def setUp(self) -> None:
        self.clear_all()

    def test_register(self):
        doc = self.user_register()
        doc["units"] = 1000
        status = self.request.post(
            self.base_url + "register", data=json.dumps(doc), headers=self.headers
        )
        self.assertEqual(status.status_code, 400)
        doc = self.user_register()
        doc.pop("user_name")
        status = self.request.post(
            self.base_url + "register", data=json.dumps(doc), headers=self.headers
        )
        self.assertEqual(status.status_code, 400)

    def test_login(self):
        doc = self.user_register()
        status = self.request.post(
            self.base_url + "register", data=json.dumps(doc), headers=self.headers
        )
        self.assertEqual(status.status_code, 201)

        creds = {"password": doc["password"], "email": doc["email"]}
        status = self.request.post(
            self.base_url + "auth/login", data=json.dumps(creds), headers=self.headers
        )

        self.assertEqual(status.status_code, 200)
        self.assertIsInstance(status.json()["access_token"], str)
        self.assertIsInstance(status.json()["refresh_token"], str)
        creds = {"password": "incorrectpassword", "email": doc["email"]}
        status = self.request.post(
            self.base_url + "auth/login", data=json.dumps(creds), headers=self.headers
        )
        self.assertEqual(status.status_code, 401)

        creds = {"password": doc["password"], "email": "incorrect email"}
        status = self.request.post(
            self.base_url + "auth/login", data=json.dumps(creds), headers=self.headers
        )
        self.assertEqual(status.status_code, 400)

    def test_protected_route(self):
        status = self.request.get(self.base_url + ME, headers=self.headers)
        self.assertEqual(status.status_code, 403)
        headers = self.headers.copy()
        headers.update({"Authorization": "Bearer Ransodasodmasd"})
        status = self.request.get(self.base_url + ME, headers=headers)
        self.assertEqual(status.status_code, 403)

        headers.update({"Authorization": None})
        status = self.request.get(self.base_url + ME, headers=headers)
        self.assertEqual(status.status_code, 403)

        doc = self.user_register()
        status = self.request.post(
            self.base_url + "register", data=json.dumps(doc), headers=self.headers
        )
        self.assertEqual(status.status_code, 201)

        creds = {"password": doc["password"], "email": doc["email"]}
        tokens = self.request.post(
            self.base_url + "auth/login", data=json.dumps(creds), headers=self.headers
        )
        headers = self.headers.copy()
        headers.update({"Authorization": f"Bearer {tokens.json()['access_token']}"})
        status = self.request.get(self.base_url + ME, headers=headers)
        self.assertEqual(status.status_code, 200)

    def tearDown(self) -> None:
        self.clear_all()
