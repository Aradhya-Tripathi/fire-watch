import os
import time

import psutil
from apis.views import JsonResponse, Throttle
from apis.views.decorators import api_view


@api_view(["GET"], [Throttle])
def health_check(request) -> JsonResponse:
    """Health check route

    Args:
        request (request): Request

    Returns:
        JsonResponse: Uptime
    """
    uptime = time.time() - psutil.Process(os.getpid()).create_time()
    return JsonResponse(data={"uptime": uptime, "OK": True}, status=200)
