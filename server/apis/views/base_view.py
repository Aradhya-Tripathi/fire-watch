from fire_watch.throttle import Throttle
from apis.views import APIView


class BaseAPIView(APIView):
    throttle_classes = [Throttle]
