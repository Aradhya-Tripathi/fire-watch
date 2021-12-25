from rest_framework.exceptions import APIException


def set_default_detail(detail):
    if not detail:
        return dict(error="Error Occurred!")
    return detail


class DuplicationError(APIException):
    def __init__(self, detail=None, status_code=409):
        detail = set_default_detail(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class EmptyUpdateClause(APIException):
    def __init__(self, detail=None, status_code=400):
        detail = set_default_detail(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class ExcessiveUnitsError(APIException):
    def __init__(self, detail=None, status_code=400):
        detail = set_default_detail(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class InvalidCredentialsError(APIException):
    def __init__(self, detail=None, status_code=401):
        detail = set_default_detail(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class InvalidToken(APIException):
    def __init__(self, detail=None, status_code=401):
        detail = set_default_detail(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class InvalidUid(APIException):
    def __init__(self, detail=None, status_code=400):
        detail = set_default_detail(detail)
        self.status_code = status_code
        super().__init__(detail=detail)


class UserDoesNotExist(APIException):
    def __init__(self, detail=None, status_code=400):
        detail = set_default_detail(detail)
        self.status_code = status_code
        super().__init__(detail)


class ConfigFileNotFound(Exception):
    def __init__(self, *args: object, path: str) -> None:
        super().__init__(f"Config file not found at the location {path}")


class SocketAuthenticationFailed(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Socket authentication failed")


class LogsNotEnabled(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Logging is disabled!!")
