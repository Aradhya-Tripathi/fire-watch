import json
from hashlib import sha256

from .base import CustomTestCase


class TestAdmin(CustomTestCase):
    def setUp(self) -> None:
        self.clear_all()

    def create_admin(self):
        self.db.AdminCredentials.insert_one(
            {
                "email": "admin@example.com",
                "password": sha256("adminpassword".encode()).hexdigest(),
            }
        )

    def test_admin_response(self):
        user_creds = self.user_login()
        headers = self.headers.copy()
        headers.update({"Authorization": f"Bearer {user_creds}"})
        user_response = self.request.get(
            self.base_url + "user/details", headers=headers
        )
        self.assertEqual(user_response.status_code, 200)
        # Assert no login through user jwt
        admin_response = self.request.get(
            self.base_url + "admin/details", headers=headers
        )
        self.assertEqual(admin_response.status_code, 403)
        admin_response = self.request.get(
            self.base_url + "admin/details", headers=self.headers
        )
        self.assertEqual(admin_response.status_code, 403)

    def test_admin_login(self):
        self.create_admin()
        admin_response = self.request.post(
            self.base_url + "admin/details",
            data=json.dumps(
                {"email": "admin@example.com", "password": "adminpassword"}
            ),
            headers=self.headers,
        )
        self.assertEqual(admin_response.status_code, 200)
        admin_creds = admin_response.json()["access_token"]
        headers = self.headers.copy()
        headers.update({"Authorization": f"Bearer {admin_creds}"})
        admin_response = self.request.get(
            self.base_url + "admin/details", headers=headers
        )
        self.assertEqual(admin_response.status_code, 200)

    def tearDown(self) -> None:
        self.clear_all()
