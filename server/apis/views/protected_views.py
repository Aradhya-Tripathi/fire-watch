import fire_watch
from apis.views import BaseAPIView, HttpRequest, JsonResponse
from apis.views.decorators import api_view


@api_view(["GET"])
def test_protected(request: HttpRequest):
    return JsonResponse(data={"Success": True}, status=200)


class UserAPI(BaseAPIView):
    def get(self, request: HttpRequest) -> JsonResponse:
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            return JsonResponse(
                {"error": f"Invalid page number {request.GET.get('page')}"}, status=400
            )
        data = request.current_user.data(page=page)
        return JsonResponse(data, status=200, safe=False)

    def delete(self, request: HttpRequest) -> JsonResponse:
        request.current_user.delete()
        fire_watch.cache.sadd("Blacklist", request.token)
        fire_watch.cache.expiremember(
            "Blacklist",
            request.token,
            fire_watch.conf.token_expiration * 60 * 60,
        )
        return JsonResponse(data={"success": True}, status=200)

    def put(self, request: HttpRequest) -> JsonResponse:
        request.current_user.update(email=request.current_user.email, doc=request.data)
        return JsonResponse(data={"success": True}, status=200)
