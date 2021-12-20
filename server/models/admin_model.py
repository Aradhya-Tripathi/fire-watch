from typing import Dict

from fire_watch.log.log_configs import get_logger

from .base_model import BaseModel


class AdminModel(BaseModel):
    logger = get_logger(__name__, filename="./alerts.log")

    def log_user_request(self, doc: Dict[str, str]):
        existing_user = self.db.Admin.find_one({"email": doc["email"]})
        #! Change to sns or ses
        if existing_user:
            self.logger.warning(f"User Update Request!")
        else:
            self.logger.warning(f"User insertion!")
        # Maintain a record of all units with users!
        self.db.Admin.insert_one(doc)
