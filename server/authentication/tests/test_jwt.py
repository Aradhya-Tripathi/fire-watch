import secrets
import unittest
from authentication.issue_jwt import TokenAuth
from datetime import timedelta


class TestJwt(unittest.TestCase):
    auth_token = TokenAuth()

    def test_jwt_creation(self):
        keys = self.auth_token.generate_key(
            payload={"user": "testuser"}, expiry=1, get_refresh=False
        )
        decoded = self.auth_token.verify_key(key=keys)
        self.assertIn("user", decoded)
        keys = self.auth_token.generate_key(
            payload={"user": "testuser"}, expiry=timedelta(hours=1), get_refresh=False
        )

        decoded = self.auth_token.verify_key(key=keys)
        self.assertIn("user", decoded)

        self.assertFalse(self.auth_token.verify_key(key=secrets.token_hex()))

    def test_refresh_creation(self):
        keys = self.auth_token.generate_key(
            payload={"user": "testuser"}, expiry=1, get_refresh=True
        )
        self.assertIn("access_token", keys)
        self.assertIn("refresh_token", keys)
