from .base import CustomTestCase


class TestRefreshToAccess(CustomTestCase):
    def setUp(self) -> None:
        self.clear_all()

    def test_successful_op(self):
        creds = self.user_login(get_refresh=True)
        headers = self.headers.copy()
        headers.update({"Authorization": f"Bearer {creds['refresh_token']}"})
        new_tokens = self.request.get(
            self.base_url + "auth/refresh", headers=headers
        ).json()
        self.assertIn("access_token", new_tokens)
        self.assertIn("refresh_token", new_tokens)

    def test_access_as_refresh(self):
        creds = self.user_login(get_refresh=True)
        headers = self.headers.copy()
        headers.update({"Authorization": f"Bearer {creds['access_token']}"})
        response = self.request.get(self.base_url + "auth/refresh", headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_invalid_tokens(self):
        headers = self.headers.copy()
        headers.update({"Authorization": "Bearer random toekn"})
        response = self.request.get(self.base_url + "auth/refresh", headers=headers)
        self.assertEqual(response.status_code, 401)

    def tearDown(self) -> None:
        self.clear_all()
