import unittest
from issue_jwt import TokenAuth


class TestJwt(unittest.TestCase):
    auth_token = TokenAuth()

    def test_jwt_creation(self):
        keys = self.auth_token.generate_key(
            payload={"user": "testuser"}, expiry=1, get_refresh=False
        )
        decoded = self.auth_token.verify_key(key=keys)
        self.assertIn("user", decoded)

    def test_refresh_creation(self):
        keys = self.auth_token.generate_key(
            payload={"user": "testuser"}, expiry=1, get_refresh=True
        )
        self.assertIn("access_token", keys)
        self.assertIn("refresh_token", keys)
