from .base import CustomTestCase
import json


class TestResetPassword(CustomTestCase):
    def setUp(self) -> None:
        self.clear_all()
        self.initial_password = "TestPassword"
        self.headers = {"Content-Type": "application/json"}
        self.user = self.user_register(password=self.initial_password)
        response = self.request.post(
            self.base_url + "apis/register",
            data=json.dumps(self.user),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 201)

    def test_reset_password(self):
        # Initialize New password
        new_password = "NewTestPassword"
        doc = {
            "email_id": self.user["email"],
            "old_passwd": self.user["password"],  # Using the new old password
            "new_passwd": new_password,  # Using the new password
        }
        response = self.request.post(
            self.base_url + "apis/reset-password",
            data=json.dumps(doc),
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)  # Assert password change success

        self.user[
            "password"
        ] = self.initial_password  # Set user password to old password
        doc = {"email": self.user["email"], "password": self.user["password"]}

        # Try logging in with old password
        response = self.request.post(
            self.base_url + "apis/login",
            data=json.dumps(doc),
            headers=self.headers,
        )
        # Assert failure
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json())

        # Try logging in with new password
        doc["password"] = new_password
        response = self.request.post(
            self.base_url + "apis/login",
            data=json.dumps(doc),
            headers=self.headers,
        )
        # Assert success
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def tearDown(self) -> None:
        self.clear_all()
