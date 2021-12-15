from django.http.response import JsonResponse
from fire_watch.config_utils import Conf
from fire_watch.errorfactory import InvalidToken

from authentication import issue_keys


class AuthMiddleWare:
    def __init__(self, view):
        self.view = view
        self._protected = ["/user/test-protected"]

    @staticmethod
    def _validate_tokentype(authorization: str):
        try:
            token_type, token = authorization.split()
            assert token_type == "Bearer"
        except (ValueError, AssertionError, AttributeError):
            raise InvalidToken({"error": "Invalid Token"})
        return token

    def authenticate_request(self, request):
        try:
            token = self._validate_tokentype(request.headers.get("Authorization"))
        except InvalidToken as e:
            return JsonResponse(data={"error": str(e)}, status=403)
        if payload := issue_keys.verify_key(key=token):
            request.auth_user = Conf(payload)
            return self.view(request)
        return JsonResponse(data={"error": "Invalid credentials"}, status=403)

    def __call__(self, request):
        if request.path in self._protected:
            return self.authenticate_request(request)
        return self.view(request)


class ReCaptchaMiddleWare:
    def __init__(self, view):
        self.view = view

    def __call__(self, request):
        return self.view(request)
