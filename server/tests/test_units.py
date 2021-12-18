import json
from typing import Dict, Union

import fire_watch

from .base import CustomTestCase


class TestUnit(CustomTestCase):
    def register_user(self, doc: Dict[str, Union[str, int]]):
        status = self.request.post(
            self.base_url + "register",
            data=json.dumps(doc),
            headers=self.headers,
        )
        return status

    def test_upload_route(self):
        self.register_user(self.user_register())

        user = self.db.users.find_one({"user_name": self.user_register()["user_name"]})
        unit_id = user["unit_id"]

        headers = self.headers.copy()
        headers.update({"Authorization": f"Bearer {unit_id}"})
        data = {
            "data": {
                "some_data": "this happened",
                "some_other_data": "this other thing happened",
            }
        }
        status = self.request.post(
            self.base_url + "upload", data=json.dumps(data), headers=headers
        )
        self.assertEqual(status.status_code, 201)

    def test_forbidden_upload(self):
        unit_id = "random"

        headers = self.headers.copy()
        headers = headers.update({"Authorization": f"Bearer {unit_id}"})
        status = self.request.post(self.base_url + "upload", headers=headers)
        self.assertEqual(status.status_code, 401)

    def test_excessive_units(self):
        doc = self.user_register(units=fire_watch.conf.max_unit_entry + 1)
        status = self.register_user(doc)
        self.assertEqual(status.status_code, 400)

    def setUp(self):
        self.clear_all()

    def tearDown(self) -> None:
        self.clear_all()
