from typing import Dict, Optional, Union

from authentication import auth_model
from fire_watch.errorfactory import DuplicationError, InvalidUid
from fire_watch.utils import pagination_utils
import fire_watch

from .base_model import BaseModel


class ApiModel(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def register_user(self, *args, **kwargs):
        auth_model.register_user(*args, **kwargs)

    def check_existing(self, doc: Dict[str, Union[str, int]]):
        """Check existing users againts the entered `email` only.

        Args:
            doc (Dict[str, Union[str, int]]): user data

        Raises:
            DuplicationError: If user exists
        """
        user = self.db.users.find_one({"email": doc["email"]})
        if user:
            raise DuplicationError({"error": "User exists!"})

    def credentials(self, *args, **kwargs):
        return auth_model.credentials(*args, **kwargs)

    def insert_data(self, unit_id: str, data: Dict[str, Union[str, int]]):
        """Insert collected data into respective unit documents.
           Insert into document if current insertions are less than
           200 else create new unit document with same unit id and
           insert.

           Can be used as a standalone function to insert data or
           through available `upload` api route

        Args:
            unit_id (str): unique unit identifier
            data (Dict[str, Union[str, int]]): data collected

        Raises:
            InvalidUid: raised if no unit found
        """
        units = list(self.db.units.find({"unit_id": unit_id}))
        try:
            unit = units.pop()
        except IndexError:
            raise InvalidUid(detail={"error": f"No unit with the id {unit_id} found"})

        if len(unit["data"]) < self.max_entry:
            self.db.units.update_one(
                {"_id": unit["_id"]}, update={"$push": {"data": data["data"]}}
            )
        else:
            doc = {"unit_id": unit_id, "data": [data["data"]]}
            self.db.units.insert_one(doc)

    def reset_password(self, **kwargs) -> None:
        auth_model.reset_password(**kwargs)

    def get_collected_data(
        self,
        page: int,
        email: Optional[str] = None,
    ):
        skip, limit = pagination_utils(
            page=page, page_limit=fire_watch.conf.pagination_limit
        )
        project_pipeline = {
            "$project": {
                "email": email,
                "_id": 0,
                "email": 0,
                "unit_id": 0,
            }
        }
        if not email:
            project_pipeline["$project"]["email"] = {}

        units = self.db.units.aggregate(
            [
                {"$limit": limit},
                {"$skip": skip},
                project_pipeline,
            ]
        )
        return units
