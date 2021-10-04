from schema import Schema, SchemaError, And


class SchoolSchema:
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

    def approval(self):
        """Validate data

        Returns:
            Union[str, Dict]: Schema check
        """
        try:
            if self.kwargs.get("register"):
                return self.register_schema.validate(self.kwargs.get("data"))
            return self.login_schema.validate(self.kwargs.get("data"))
        except SchemaError as e:
            return {"error": str(e)}
