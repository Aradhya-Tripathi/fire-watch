import os
import unittest
from fire_watch.log.log_configs import get_logger


class TestLog(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logger = get_logger(__name__, filename="./test.log", level=10)

    def test_logger(self):
        message = "this is a logging message"
        self.logger.debug(message)
        self.assertTrue(os.path.exists("./test.log"))

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("./test.log")
