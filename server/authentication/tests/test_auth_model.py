import unittest
from dotenv import load_dotenv
from authentication.models import AuthModel
from authentication import utils
from fire_watch.errorfactory import InvalidUid


class TestAuthModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        load_dotenv()
        cls.auth_model = AuthModel()

    def setUp(self) -> None:
        self.auth_model.db.units.insert_one({"unit_id": "randomunit_id"})

    def test_validate_token(self):
        self.assertTrue(utils.validate_unit_id("randomunit_id"))

    def test_invalid_token(self):
        with self.assertRaises(InvalidUid) as error:
            utils.validate_unit_id("invalidunit_id")

    def tearDown(self) -> None:
        self.auth_model.db.units.remove({"unit_id": "randomunit_id"})
