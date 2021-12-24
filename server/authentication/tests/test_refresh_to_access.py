from unittest import TestCase

from authentication.issue_jwt import TokenAuth


class TestAccessToRefresh(TestCase):
    auth_token = TokenAuth()

    def test_access_token_as_refresh(self):
        tokens = self.auth_token.generate_key(
            payload={"user": "TestUser", "age": 10}, get_refresh=True, is_admin=True
        )
        check = self.auth_token.refresh_to_access(key=tokens["access_token"])
        self.assertIsNone(check)

    def test_successful_op(self):
        tokens = self.auth_token.generate_key(
            payload={"user": "TestUser", "age": 10}, get_refresh=True, is_admin=True
        )
        check = self.auth_token.refresh_to_access(key=tokens["refresh_token"])
        self.assertIsNotNone(check)
        payload = self.auth_token.verify_key(is_admin=True, key=check["access_token"])
        self.assertEqual(payload["user"], "TestUser")
        self.assertEqual(payload["age"], 10)
        self.assertEqual(payload["is_admin"], True)
        self.assertEqual(payload.get("refresh"), None)

        payload = self.auth_token.verify_key(is_admin=True, key=check["refresh_token"])
        self.assertEqual(payload["user"], "TestUser")
        self.assertEqual(payload["age"], 10)
        self.assertEqual(payload["is_admin"], True)
        self.assertEqual(payload["refresh"], True)
