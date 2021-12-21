from .base import CustomTestCase


class TestAdmin(CustomTestCase):
    def setUp(self) -> None:
        self.clear_all()

    def test_admin_response(self):
        user_creds = self.user_login()
        headers = self.headers.copy()
        headers.update({"Authorization": f"Bearer {user_creds}"})
        user_response = self.request.get(
            self.base_url + "user/details", headers=headers
        )
        self.assertEqual(user_response.status_code, 200)
        # Assert no login through user jwt
        admin_response = self.request.get(self.base_url + "admin", headers=headers)
        self.assertEqual(admin_response.status_code, 403)
        admin_response = self.request.get(self.base_url + "admin", headers=self.headers)
        self.assertEqual(admin_response.status_code, 403)

    def tearDown(self) -> None:
        self.clear_all()
