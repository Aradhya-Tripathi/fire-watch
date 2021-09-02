from rest_framework.views import APIView
from django.http.response import JsonResponse
import os
import psutil
import time


class HealthCheck(APIView):
    def get(self, request, **kwargs):
        uptime = time.time() - psutil.Process(os.getpid()).create_time()
        return JsonResponse(data={"uptime": uptime, "OK": True}, status=200)
