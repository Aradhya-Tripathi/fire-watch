import os

import jwt
from dotenv import load_dotenv

from .base import CustomTestCase

load_dotenv()


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
        new_payload = jwt.decode(
            new_tokens["access_token"],
            key=os.getenv("SECRET_KEY"),
            algorithms=["HS256"],
        )

        old_payload = jwt.decode(
            creds["access_token"],
            key=os.getenv("SECRET_KEY"),
            algorithms=["HS256"],
        )

        new_refresh_payload = jwt.decode(
            new_tokens["refresh_token"],
            key=os.getenv("SECRET_KEY"),
            algorithms=["HS256"],
        )

        old_refresh_payload = jwt.decode(
            creds["refresh_token"],
            key=os.getenv("SECRET_KEY"),
            algorithms=["HS256"],
        )

        self.assertEqual(new_refresh_payload["email"], old_refresh_payload["email"])
        self.assertEqual(
            new_refresh_payload["is_admin"], old_refresh_payload["is_admin"]
        )
        self.assertEqual(new_refresh_payload.get("refresh"), True)

        self.assertEqual(new_payload["email"], old_payload["email"])
        self.assertEqual(new_payload["is_admin"], old_payload["is_admin"])
        self.assertEqual(new_payload.get("refresh"), None)

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
