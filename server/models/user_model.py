from typing import Any, Dict

from apis.utils import pagination_utils
from fire_watch.errorfactory import UserDoesNotExist

from models.api_model import ApiModel


class User(ApiModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_name = kwargs["user_name"]
        self.email = kwargs["email"]
        self.max_size = kwargs.get("max_size", 10)

    def __repr__(self) -> str:
        return self.user_name

    def __str__(self) -> str:
        return self.user_name

    @property
    def user_details(self):
        return self.user_name, self.email

    @property
    def total_units(self):
        user = self.db.users.find_one({"email": self.email})
        return user["units"]

    @property
    def user(self):
        return self.user_name

    def user_data(self, page):
        skip = pagination_utils(page, self.max_size)
        if data := self.get_collected_data(
            email=self.email, max_size=self.max_size, skip=skip
        ):
            return list(data)

    def delete(self):
        user_doc = self.db.users.delete_one({"email": self.email})
        if user_doc:
            self.db.units.delete_many({"unit_id": user_doc["unit_id"]})
        raise UserDoesNotExist({"error": "User already removed!"})

    def update_user(self, email: str, doc: Dict[str, Any]):
        original_doc = self.db.users.find_one({"email": email})
        if not original_doc:
            UserDoesNotExist({"error": "User does not exist!"})

        changes = dict()
        self.check_excessive_units(doc.get("units", 0))
        for key, value in original_doc.items():
            if key in doc and doc[key] != value:
                changes.update({key: doc[key]})

        if changes:
            self.db.users.find_one_and_update(
                {"email": email},
                {"$set": changes},
            )
