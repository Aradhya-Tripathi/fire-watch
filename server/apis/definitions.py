from schema import And, Schema, SchemaError


class UserSchema:
    def __init__(self, *args, **kwargs):

        self.kwargs = kwargs

        self.register_schema = Schema(
            schema={
                "user_name": And(str, lambda name: len(name.strip()) > 0),
                "units": And(int, lambda units: units > 0),
                "password": And(str, lambda passwd: len(passwd.strip()) > 0),
                "email": And(str, lambda email: len(email.strip()) > 0),
            }
        )
        self.login_schema = Schema(
            schema={
                "password": And(str, lambda passwd: len(passwd.strip()) > 0),
                "email": And(str, lambda email: len(email.strip()) > 0),
            }
        )

        self.reset_password_schema = Schema(
            schema={
                "old_passwd": And(str, lambda old_pswd: len(old_pswd.strip()) > 0),
                "new_passwd": And(str, lambda new_pswd: len(new_pswd.strip()) > 0),
                "email_id": And(str, lambda eamil_id: len(eamil_id.strip()) > 0),
            }
        )

    def approval(self):
        """Validate data

        Returns:
            Union[str, Dict]: Schema check
        """
        try:
            if self.kwargs.get("register"):
                return self.register_schema.validate(self.kwargs.get("data"))
            elif self.kwargs.get("reset"):
                return self.reset_password_schema.validate(self.kwargs.get("data"))
            return self.login_schema.validate(self.kwargs.get("data"))
        except SchemaError as e:
            return {"error": str(e)}
