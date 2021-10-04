class DuplicationError(Exception):
    ...


class ExcessiveUnitsError(Exception):
    def __init__(self, *args: object, units: int) -> None:
        super().__init__(f"Unit limit excede {units}")


class InvalidCredentialsError(Exception):
    ...


class InvalidToken(Exception):
    ...


class InvalidUid(Exception):
    ...


class ConfigFileNotFound(Exception):
    def __init__(self, *args: object, path: str) -> None:
        super().__init__(f"Config file not found at the location {path}")


class SocketAuthenticationFailed(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Socket authentication failed")


class LogsNotEnabled(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Logging is disabled!!")