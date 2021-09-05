import os
import time

import psutil
from authentication import issue_keys
from core.throttle import throttle
from django.http import request
from django.http.response import JsonResponse
from rest_framework.views import APIView

from .checks import enter_school, login
from .definitions import SchoolSchema


class HealthCheck(APIView):
    throttle_classes = [throttle]

    def get(self, request: request, **kwargs) -> JsonResponse:
        """Health check route

        Args:
            request (request): Request

        Returns:
            JsonResponse: Uptime
        """
        uptime = time.time() - psutil.Process(os.getpid()).create_time()
        return JsonResponse(data={"uptime": uptime, "OK": True}, status=200)


class Register(APIView):
    throttle_classes = [throttle]

    def post(self, request: request, **kwargs) -> JsonResponse:
        """Register schools

        Args:
            request (request): wsgi request

        Returns:
            JsonResponse: Response
        """
        validate = SchoolSchema(data=request.data, register=True).approval()

        if "error" in validate:
            return JsonResponse(data={"error": validate["error"]}, status=400)

        if value := enter_school(validate):
            return JsonResponse(data={"error": str(value)}, status=400)

        return JsonResponse(data={"success": True}, status=201)


class Login(APIView):
    throttle_classes = [throttle]

    def post(self, request, **kwargs):
        validate = SchoolSchema(data=request.data).approval()

        if "error" in validate:
            return JsonResponse(data={"error": validate["error"]}, status=400)

        creds = login(password=validate.get("password"), email=validate.get("email"))

        if isinstance(creds, str):
            return JsonResponse(data={"error": creds}, status=403)
        payload = {"school_name": creds["school_name"]}
        access_token, refresh_token = issue_keys.generate_key(
            payload=payload, expiry=1, get_refresh=True, refresh_exipry=12
        )
        return JsonResponse(
            data={"access_token": access_token, "refresh_token": refresh_token},
            status=200,
        )
