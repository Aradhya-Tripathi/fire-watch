from rest_framework.throttling import AnonRateThrottle


class throttle(AnonRateThrottle):

    scope = "basic_throttle"

    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)
