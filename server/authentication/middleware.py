from authentication import issue_keys
from django.http.response import JsonResponse


class AuthMiddleWare:
    def __init__(self, view):
        self.view = view
        self._protected = ["/apis/protected"]

    def authenticate_request(self, request):
        if issue_keys.verify_key(key=request.headers.get("Authorization")):
            return JsonResponse(data={"error": "Invalid credentials"}, status=403)
        return self.view(request)

    def __call__(self, request):
        if request.path in self._protected:
            return self.authenticate_request(request)
        return self.view(request)


class ReCaptchaMiddleWare:
    def __init__(self, view):
        self.view = view

    def __call__(self, request):
        return self.view(request)
