from authentication import issue_keys
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

    def authenticate(self, scope):
        try:
            authorization = self.get_credentials(scope["headers"])
        except InvalidToken as e:
            scope["error"] = str(e)
            return scope
        try:
            token_type, token = authorization
            assert token_type == "Bearer"
            if key := issue_keys.verify_key(key=token):
                scope["current"] = key
            else:
                raise InvalidCredentialsError("Invalid token")
        except Exception as e:
            scope["error"] = str(e)

        return scope

    async def __call__(self, scope, recieve, send):
        if scope["path"] in self._protected:
            scope = self.authenticate(scope)
        return await self.view(scope, recieve, send)
