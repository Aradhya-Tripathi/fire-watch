from apis.views import APIView, JsonResponse, Throttle
from apis.views.decorators import api_view


@api_view(["GET"], [Throttle])
def test_protected(request):
    return JsonResponse(data={"Success": True}, status=200)


class UserAPI(APIView):
    throttle_classes = [Throttle]

    def get(self, request):
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            return JsonResponse(
                {"error": f"Invalid page number {request.GET.get('page')}"}, status=400
            )
        data = request.user.user_data(page=page)
        response = data if data else dict(detail="No data found!")
        return JsonResponse(response, status=200, safe=False)

    def delete(self, request):
        request.user.delete()
