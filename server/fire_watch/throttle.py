from rest_framework.throttling import AnonRateThrottle


class Throttle(AnonRateThrottle):

    scope = "basic_throttle"

    def allow_request(self, request, view):
        if request.method == "GET" and request.path != "auth/refresh":
            return True
        return super().allow_request(request, view)
