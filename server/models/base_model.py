import random
import string

import fire_watch
from fire_watch.errorfactory import ExcessiveUnitsError


class BaseModel:
    user_model = {
        "user_name": str,
        "password": str,
        "email": str,
        "units": int,
        "unit_id": str,
    }
    units_model = {
        "unit_id": str,
        "data": list,
    }

    max_entry = fire_watch.conf.max_unit_entry
    db = fire_watch.db

    def get_uid(self, length: int):
        """Get unique UID for a document.

        Args:
            length (int, optional): length of uuid. Defaults to 8.

        Returns:
            str: uuid
        """
        uid = random.choices(string.ascii_uppercase, k=length)
        if self.db.collection.find_one({"_id": uid}):
            return self.get_uid()
        return "".join(uid)

    def check_excessive_units(self, units):
        if units > self.max_entry:
            raise ExcessiveUnitsError(
                detail={
                    "error": f"Excessive no. of units {units} current max units are {self.max_entry}"
                }
            )
