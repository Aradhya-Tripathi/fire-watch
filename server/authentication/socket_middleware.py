from typing import Any, Dict
from authentication import issue_keys, auth_model
from core.errorfactory import InvalidToken, InvalidCredentialsError


class AuthMiddleWare:
    def __init__(self, view):
        self.view = view
        self._protected = ["/alerts"]

    @staticmethod
    def get_credentials(headers):
        for header in headers:
            if isinstance(header, tuple):
                key, value = header[0].decode(), header[1].decode()
                if key == "authorization":
                    return value.split()
        raise InvalidToken("Token not provided")

    def authenticate(self, scope: Dict[str, Any]) -> Dict[str, Any]:
        """Middleware authentication for sockets adds `error` message in scope
           if authentication failed else adds `current` in scope representing the
           current user (unit_id).

        Args:
            scope (Dict[str, Any]): Incoming scope

        Raises:
            InvalidCredentialsError: Raised when authentication fails

        Returns:
            Dict[str, Any]: returns modified scope
        """
        try:
            authorization = self.get_credentials(scope["headers"])
        except InvalidToken as e:
            scope["error"] = str(e)
            return scope
        try:
            token_type, token = authorization
            assert token_type == "Bearer"
            if key := issue_keys.verify_key(key=token):
                scope["current"] = auth_model.id_from_user(key["user_name"])
            else:
                raise InvalidCredentialsError("Invalid token")
        except Exception as e:
            scope["error"] = str(e)

        return scope

    async def __call__(self, scope, recieve, send):
        if scope["path"] in self._protected:
            scope = self.authenticate(scope)
        return await self.view(scope, recieve, send)
