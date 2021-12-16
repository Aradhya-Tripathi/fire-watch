import json

from .base import CustomTestCase


class UserTests(CustomTestCase):
    def setUp(self) -> None:
        self.clear_all()

    def test_user_data(self):
        headers = {"Content-Type": "application/json"}
        user_doc = self.user_register()
        response = self.request.post(
            self.base_url + "register", data=json.dumps(user_doc), headers=headers
        )
        login_response = self.request.post(
            self.base_url + "login",
            data=json.dumps(
                {"email": user_doc["email"], "password": user_doc["password"]}
            ),
            headers=headers,
        )
        self.assertEqual(login_response.status_code, 200)
        user_creds = login_response.json()["access_token"]
        details_response = self.request.get(
            self.base_url + "user/details", headers=headers
        )
        self.assertEqual(details_response.status_code, 403)
        headers.update({"Authorization": f"Bearer {user_creds}"})
        details_response = self.request.get(
            self.base_url + "user/details", headers=headers
        )
        # self.assertEqual(details_response.json(), {"details": "No data found!"})
        self.assertEqual(details_response.status_code, 200)

        self.assertEqual(response.status_code, 201)
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

    def test_user_removal(self):
        ...

    def tearDown(self) -> None:
        self.clear_all()
