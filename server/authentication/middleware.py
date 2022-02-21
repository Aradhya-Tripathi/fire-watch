from typing import Any, Dict

import fire_watch
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from fire_watch.config_utils import Conf
from fire_watch.errorfactory import InvalidToken
from models.user_model import User
from rest_framework.views import APIView

from authentication import issue_keys
from authentication.utils import get_token


class AuthMiddleWare:
    def __init__(self, view):
        self.view = view
        self._protected = "/user"
        self._admin_path = "/admin"

    def attach_objects(
        self,
        payload: Dict[str, Any],
        token: str,
        is_admin: bool,
    ):

        setattr(
            self.request, "current_admin" if is_admin else "current_user", Conf(payload)
        )
        self.request.is_admin = is_admin
        self.request.token = token

    def attach_user(self, request: HttpRequest):
        """Attach the user object to `request.user` if in view UserAPI
        and user is authenticated.

        Args:
            request (request): request object
        """
        if request.path == "/user/details":
            request.current_user = User(
                user_name=request.current_user.user_name,
                email=request.current_user.email,
                max_size=fire_watch.conf.pagination_limit["debug"]
                if fire_watch.flags.in_debug
                else fire_watch.conf.pagination_limit["production"],
            )

    def authenticate_user_request(self) -> APIView:
        """Authenticate each request made to a protected route.

        Args:
            request (request): request object

        Returns:
            APIView: handler method.
        """

        try:
            token = get_token(self.request.headers)
        except InvalidToken as e:
            return JsonResponse(data={"error": "Invalid token type!"}, status=403)
        if (
            payload := issue_keys.verify_key(key=token, is_admin=False)
        ) and not fire_watch.cache.sismember("Blacklist", token):
            self.attach_objects(
                is_admin=False,
                payload=payload,
                token=token,
            )
            #! Warning: Only attach user object after authentication!
            self.attach_user(self.request)
            return self.view(self.request)
        return JsonResponse(data={"error": "Invalid credentials"}, status=403)

    def admin_login_route(self, request):
        #! Allow access to admin login route.
        return request.path == "/admin/details" and request.method == "POST"

    def authenticate_admin_request(self):
        """Authenticate each request made to a admin route.

        Args:
            request (request): request object

        Returns:
            APIView: handler method.
        """
        if self.admin_login_route(self.request):
            return self.view(self.request)
        try:
            token = get_token(self.request.headers)
        except InvalidToken as e:
            return JsonResponse(data={"error": str(e)}, status=403)
        if (
            payload := issue_keys.verify_key(key=token, is_admin=True)
        ) and not fire_watch.cache.sismember("Blacklist", token):
            self.attach_objects(
                payload=payload,
                token=token,
                is_admin=True,
            )
            return self.view(self.request)
        return JsonResponse(data={"error": "Invalid credentials"}, status=403)

    def __call__(self, request):
        self.request = request
        if self._admin_path in request.path:
            return self.authenticate_admin_request()

        if self._protected in request.path:
            return self.authenticate_user_request()

        return self.view(request)
