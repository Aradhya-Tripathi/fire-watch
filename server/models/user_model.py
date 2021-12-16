from models.api_model import Model
from fire_watch.errorfactory import UserDoesNotExist
from apis.utils import pagination_utils


class User(Model):
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
            self.email, max_size=self.max_size, skip=skip
        ):
            return list(data)

    def delete(self):
        user_doc = self.db.users.delete_one({"email": self.email})
        if user_doc:
            self.db.units.delete_many({"unit_id": user_doc["unit_id"]})
        raise UserDoesNotExist({"error": "User already removed!"})
