import secrets
import unittest
from authentication.issue_jwt import AuthToken
from datetime import timedelta


class TestJwt(unittest.TestCase):
    auth_token = AuthToken()

    def test_jwt_creation(self):
        keys = self.auth_token.generate_key(
            payload={"user": "testuser"},
            expiry=1,
            get_refresh=False,
            is_admin=False,
        )
        decoded = self.auth_token.verify_key(key=keys, is_admin=False)
        incorrect = self.auth_token.verify_key(key=keys, is_admin=True)
        self.assertEqual(incorrect, None)
        self.assertIn("user", decoded)
        keys = self.auth_token.generate_key(
            payload={"user": "testuser"},
            expiry=timedelta(hours=1),
            get_refresh=False,
            is_admin=True,
        )

        decoded = self.auth_token.verify_key(key=keys, is_admin=True)
        self.assertIn("user", decoded)
        self.assertEqual(decoded["is_admin"], True)

        self.assertFalse(
            self.auth_token.verify_key(key=secrets.token_hex(), is_admin=False)
        )

    def test_refresh_creation(self):
        keys = self.auth_token.generate_key(
            payload={"user": "testuser"},
            expiry=1,
            get_refresh=True,
            is_admin=False,
        )
        self.assertIn("access_token", keys)
        self.assertIn("refresh_token", keys)
