from apis.views import BaseAPIView, JsonResponse, Throttle
from apis.views.decorators import api_view


@api_view(["GET"])
def test_protected(request):
    return JsonResponse(data={"Success": True}, status=200)


class UserAPI(BaseAPIView):
    def get(self, request):
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            return JsonResponse(
                {"error": f"Invalid page number {request.GET.get('page')}"}, status=400
            )
        data = request.current_user.user_data(page=page)
        response = data if data else dict(detail="No data found!")
        return JsonResponse(response, status=200, safe=False)

    def delete(self, request):
        request.current_user.delete()
        return JsonResponse(data={"success": True}, status=200)

    def put(self, request):
        ...
