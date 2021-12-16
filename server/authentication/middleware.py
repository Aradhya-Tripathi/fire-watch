import fire_watch
from models.user_model import User
from django.http import request
from django.http.response import JsonResponse
from fire_watch.config_utils import Conf
from fire_watch.errorfactory import InvalidToken
from rest_framework.views import APIView

from authentication import issue_keys
from authentication.utils import get_token


class AuthMiddleWare:
    def __init__(self, view):
        self.view = view
        self._protected = "/user"

    def attach_user(self, request: request):
        """Attach the user object to `request.user` if in view UserAPI
        and user is authenticated.

        Args:
            request (request): request object
        """
        if request.path == "/user/details" and request.user.authorized:
            request.user = User(
                user_name=request.auth_user.user_name,
                email=request.auth_user.email,
                max_size=fire_watch.conf.pagination_limit["debug"]
                if fire_watch.flags.in_debug
                else fire_watch.conf.pagination_limit["production"],
            )

    def authenticate_request(self, request: request) -> APIView:
        """Authenticate each request made to a protected route.

        Args:
            request (request): request object

        Returns:
            APIView: handler method.
        """

        try:
            token = get_token(request.headers)
        except InvalidToken as e:
            return JsonResponse(data={"error": str(e)}, status=403)
        if payload := issue_keys.verify_key(key=token):
            request.user.authorized = True
            request.auth_user = Conf(payload)
            # Warning: Only attach user object after authentication!
            self.attach_user(request)
            return self.view(request)
        request.user.authorized = False
        return JsonResponse(data={"error": "Invalid credentials"}, status=403)

    def __call__(self, request):
        if self._protected in request.path:
            return self.authenticate_request(request)
        return self.view(request)


class ReCaptchaMiddleWare:
    def __init__(self, view):
        self.view = view

    def __call__(self, request):
        # todo: Add recaptcha
        fire_watch.flags.recaptcha_enabled = False
        return self.view(request)
