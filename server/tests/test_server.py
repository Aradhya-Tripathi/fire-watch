from unittest import TestCase
import requests


class TestServerBoot(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Start server
        """
        cls.request = requests.Session()
        cls.base_url = "http://localhost:8000/"

    def test_server(self):
        status = self.request.get(self.base_url + "apis/healthcheck")
        self.assertEqual(200, status.status_code)
