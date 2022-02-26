import uuid

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

    def get_uid(self):
        """Get unique UID for a document."""
        return uuid.uuid4().hex

    def check_excessive_units(self, units):
        if units > self.max_entry:
            raise ExcessiveUnitsError(
                detail={
                    "error": f"Excessive no. of units {units} current max units are {self.max_entry}"
                }
            )
