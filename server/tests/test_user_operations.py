import json

from .base import CustomTestCase


class UserTests(CustomTestCase):
    def setUp(self) -> None:
        self.clear_all()

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

    def update(self, data, user_creds, invalid_user=False):
        headers = self.headers.copy()
        if not invalid_user:
            headers.update({"Authorization": f"Bearer {user_creds}"})
        else:
            headers.update({"Authorization": f"Bearer {None}"})

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
        self.assertEqual(response.status_code, 400)

        data = {"user_name": "NewName"}
        response = self.update(data, user_creds)
        self.assertEqual(response.status_code, 200)

    def test_user_deletion(self):
        user_creds = self.user_login()
        headers = self.headers.copy()
        headers.update({"Authorization": f"Bearer {user_creds}"})
        response = self.request.delete(self.base_url + "user/details", headers=headers)
        self.assertEqual(response.status_code, 200)

        data = {"units": 1, "user_name": "OtherUser"}
        response = self.update(data, user_creds)
        self.assertEqual(response.status_code, 403)

    def tearDown(self) -> None:
        self.clear_all()
