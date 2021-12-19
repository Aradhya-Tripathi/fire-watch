import json

from .base import CustomTestCase


class UserTests(CustomTestCase):
    def setUp(self) -> None:
        self.clear_all()

    def user_login(self):
        user_doc = self.user_register()
        response = self.request.post(
            self.base_url + "register", data=json.dumps(user_doc), headers=self.headers
        )
        self.assertEqual(response.status_code, 201)

        login_response = self.request.post(
            self.base_url + "login",
            data=json.dumps(
                {"email": user_doc["email"], "password": user_doc["password"]}
            ),
            headers=self.headers,
        )
        self.assertEqual(login_response.status_code, 200)
        user_creds = login_response.json()["access_token"]
        return user_creds

    def test_user_data(self):
        user_creds = self.user_login()
        details_response = self.request.get(
            self.base_url + "user/details", headers=self.headers
        )
        self.assertEqual(details_response.status_code, 403)
        headers = self.headers.copy()
        headers.update({"Authorization": f"Bearer {user_creds}"})
        details_response = self.request.get(
            self.base_url + "user/details", headers=headers
        )
        self.assertEqual(details_response.json(), [{"data": []}])
        self.assertEqual(details_response.status_code, 200)

        user = self.db.users.find_one({"user_name": self.user_register()["user_name"]})
        unit_id = user["unit_id"]
        headers.update({"Authorization": f"Bearer {unit_id}"})
        data_dump = {"data": {"temp": 201, "other data": "other value"}}
        status = self.request.post(
            self.base_url + "upload",
            headers=headers,
            data=json.dumps(data_dump),
        )
        self.assertEqual(status.status_code, 201)

        headers.update({"Authorization": f"Bearer {user_creds}"})
        details_response = self.request.get(
            self.base_url + "user/details", headers=headers
        )
        expected_response = [{"data": [{"temp": 201, "other data": "other value"}]}]
        self.assertEqual(details_response.json(), expected_response)

    def update(self, data, user_creds):
        headers = self.headers.copy()
        headers.update({"Authorization": f"Bearer {user_creds}"})
        response = self.request.put(
            self.base_url + "user/details", data=json.dumps(data), headers=headers
        )
        return response

    def test_user_update(self):
        user_creds = self.user_login()
        data = {"units": 100}
        response = self.update(data, user_creds)
        self.assertEqual(response.status_code, 200)

        data = {"units": 1, "user_name": "OtherUser"}
        response = self.update(data, user_creds)
        self.assertEqual(response.status_code, 200)

        data = {"units": 1000, "user_name": "OtherUser"}
        response = self.update(data, user_creds)
        self.assertEqual(response.status_code, 400)

        data = {"user_name": "OtherUser"}
        response = self.update(data, user_creds)
        self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        self.clear_all()
