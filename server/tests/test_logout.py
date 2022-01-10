import json

from .base import CustomTestCase


class TestLogout(CustomTestCase):
    def setUp(self) -> None:
        self.clear_all()

    def test_logout(self):
        creds = self.user_login(get_refresh=True)
        headers = self.headers.copy()
        headers.update(
            {"Authorization": f"Bearer {creds['access_token']}"},
        )
        response = self.request.get(
            self.base_url + "user/details",
            headers=headers,
        )
        self.assertEqual(response.status_code, 200)
        self.request.post(
            self.base_url + "auth/logout",
            data=json.dumps(creds),
            headers=self.headers,
        )

        response = self.request.get(
            self.base_url + "user/details",
            headers=headers,
        )
        self.assertEqual(response.status_code, 403)

    def tearDown(self) -> None:
        self.clear_all()
