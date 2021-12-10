from datetime import timedelta

from apis.transactions import login, reset_password
from apis.definitions import UserSchema
from core.throttle import Throttle
from django.http import request
from django.http.response import JsonResponse
from rest_framework.views import APIView

from . import issue_keys


class Login(APIView):
    throttle_classes = [Throttle]

    def post(self, request: request, **kwargs) -> JsonResponse:
        """Login users

        Args:
            request (request): wsgi request

        Returns:
            JsonResponse: Response
        """
        validate = UserSchema(data=request.data).approval()

        if "error" in validate:
            return JsonResponse(data={"error": validate["error"]}, status=400)

        creds = login(password=validate.get("password"), email=validate.get("email"))

        payload = {"user_name": creds["user_name"]}
        key = issue_keys.generate_key(
            payload=payload,
            expiry=timedelta(hours=1),
            get_refresh=True,
            refresh_exipry=timedelta(hours=12),
        )
        return JsonResponse(
            data={
                "access_token": key["access_token"],
                "refresh_token": key["refresh_token"],
            },
            status=200,
        )


class ResetPassword(APIView):
    throttle_classes = [Throttle]

    def post(self, request: request, **kwargs) -> JsonResponse:
        """Allow reset password

        Args:
            request (request): wsgi request

        Returns:
            JsonResponse: Response
        """
        validate = UserSchema(data=request.data, reset=True).approval()
        if "error" in validate:
            return JsonResponse(data={"error": validate["error"]}, status=400)
        reset_password(request.data)
        return JsonResponse(data={}, status=200)
