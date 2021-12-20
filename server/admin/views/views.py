from apis.views import BaseAPIView, JsonResponse, request


class AdminView(BaseAPIView):
    def get(self, request: request):
        return JsonResponse({"success": True}, statu=200)
