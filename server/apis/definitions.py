import re
from typing import Optional, Dict

from schema import And, Schema, SchemaError

email_re = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


class UserSchema:
    def __init__(self, *args, **kwargs):

        self.kwargs = kwargs
        self.email_re = email_re

        self.register_schema = Schema(
            schema={
                "user_name": And(str, lambda name: len(name.strip()) > 0),
                "units": And(int, lambda units: units > 0),
                "password": And(str, lambda passwd: len(passwd.strip()) > 0),
                "email": And(str, lambda email: self.email_re.fullmatch(email)),
            }
        )
        self.login_schema = Schema(
            schema={
                "password": And(str, lambda passwd: len(passwd.strip()) > 0),
                "email": And(str, lambda email: self.email_re.fullmatch(email)),
            }
        )

        self.reset_password_schema = Schema(
            schema={
                "old_passwd": And(str, lambda old_pswd: len(old_pswd.strip()) > 0),
                "new_passwd": And(str, lambda new_pswd: len(new_pswd.strip()) > 0),
                "email_id": And(
                    str,
                    lambda email: self.email_re.fullmatch(email),
                ),
            }
        )

        self.collect_data = Schema(schema={"data": dict})

        self.modify_user_details = Schema(
            schema={
                "units": Optional[int],
                "user_name": Optional[str],
            }
        )

    def approval(self):
        """Validate data

        Returns:
            Union[str, Dict]: Schema check
        """
        try:
            #! Fix this
            if not self.kwargs.get("data").values():
                raise SchemaError("No data provided")
            if self.kwargs.get("register"):
                return self.register_schema.validate(self.kwargs.get("data"))
            elif self.kwargs.get("reset"):
                return self.reset_password_schema.validate(self.kwargs.get("data"))
            elif self.kwargs.get("upload"):
                return self.collect_data.validate(self.kwargs.get("data"))
            elif self.kwargs.get("user_update"):
                return self.modify_user_details.validate(self.kwargs.get("data"))
            else:
                return self.login_schema.validate(self.kwargs.get("data"))
        except SchemaError as e:
            return {"error": str(e)}


class AdminSchema:
    def __init__(self, data: Dict[str, str]):
        self.admin_login = Schema(
            schema={
                "email": And(str, lambda email: self.email_re.fullmatch(email)),
                "password": str,
            }
        )
        self.data = data

    def approval(self):
        try:
            self.admin_login.validate(self.data)
        except SchemaError as e:
            return {"error": str(e)}
