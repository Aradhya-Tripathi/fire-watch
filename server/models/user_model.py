from typing import Any, Dict

from admin import admin_model
from apis import model as api_model
from fire_watch.errorfactory import EmptyUpdateClause, UserDoesNotExist

from .base_model import BaseModel


class User(BaseModel):
    def __init__(self, *args, **kwargs):
        self.user_name = kwargs["user_name"]
        self.email = kwargs["email"]
        self._user = self.db.users.find_one({"email": self.email})

    def __repr__(self) -> str:
        return self.user_details

    def __str__(self) -> str:
        return self.user_details

    @property
    def user_details(self):
        return self.user_name, self.email

    @property
    def total_units(self):
        return self._user["units"]

    @property
    def unit_id(self):
        return self._user["unit_id"]

    @property
    def user(self):
        return self.user_name

    def data(self, page):
        if data := api_model.get_collected_data(
            unit_id=self.unit_id,
            page=page,
        ):
            return list(data)

    def delete(self):
        user_doc = self.db.users.delete_one({"email": self.email})
        if user_doc.deleted_count:
            self.db.units.delete_many({"unit_id": self.unit_id})
            return
        raise UserDoesNotExist({"error": "User already removed!"})

    def update(self, email: str, doc: Dict[str, Any]):
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
            admin_model.log_user_request({"email": email, "updates": changes})
            return
        raise EmptyUpdateClause(detail={"error": "Nothing to update!"})
