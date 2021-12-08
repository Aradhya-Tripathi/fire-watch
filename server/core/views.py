import os
import time

import psutil
from django.http.response import JsonResponse
from rest_framework.views import APIView

from .throttle import Throttle


class HealthCheck(APIView):
    throttle_classes = [Throttle]

    def get(self, request) -> JsonResponse:
        """Health check route

        Args:
            request (request): Request

        Returns:
            JsonResponse: Uptime
        """
        uptime = time.time() - psutil.Process(os.getpid()).create_time()
        return JsonResponse(data={"uptime": uptime, "OK": True}, status=200)
