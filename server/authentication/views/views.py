from datetime import timedelta

from apis.definitions import UserSchema
from authentication.utils import login, reset_password
from apis.views import BaseAPIView, JsonResponse, HttpRequest

from .. import issue_keys


class Login(BaseAPIView):
    def post(self, request: HttpRequest) -> JsonResponse:
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

        payload = {"user_name": creds["user_name"], "email": creds["email"]}
        key = issue_keys.generate_key(
            payload=payload,
            expiry=timedelta(hours=1),
            get_refresh=True,
            refresh_exipry=timedelta(hours=12),
            is_admin=False,
        )
        return JsonResponse(
            data={
                "access_token": key["access_token"],
                "refresh_token": key["refresh_token"],
            },
            status=200,
        )


class ResetPassword(BaseAPIView):
    def post(self, request: HttpRequest) -> JsonResponse:
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
