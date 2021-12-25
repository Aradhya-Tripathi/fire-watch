from typing import Dict

from schema import And, Schema, SchemaError


def logout_schema(data: Dict[str, str]):
    schema = Schema(
        schema={
            "access_token": And(str, lambda token: len(token.strip()) > 0),
            "refresh_token": And(str, lambda token: len(token.strip()) > 0),
        }
    )

    try:
        return schema.validate(data)
    except SchemaError as e:
        return str(e)
