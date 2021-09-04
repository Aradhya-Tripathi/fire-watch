import os
import time

import psutil
from django.http import request
from django.http.response import JsonResponse
from rest_framework.views import APIView

from .checks import enter_school
from .definitions import SchoolSchema


class HealthCheck(APIView):
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
    def post(self, request: request, **kwargs) -> JsonResponse:
        """Register schools

        Args:
            request (request): wsgi request

        Returns:
            JsonResponse: Response
        """
        validate = SchoolSchema(data=request.data, register=True).approval()

        if "error" in validate:
            return JsonResponse(data={'error': validate["error"]}, status=400)

        if value := enter_school(validate):
            return JsonResponse(data={"error": str(value)}, status=400)

        return JsonResponse(data={"success": True}, status=201)
