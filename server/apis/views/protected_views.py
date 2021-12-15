from apis.user_model import User
from apis.views import APIView, JsonResponse, Throttle
from apis.views.decorators import api_view


@api_view(["GET"], [Throttle])
def test_protected(request):
    return JsonResponse(data={"Success": True}, status=200)


class UserData(APIView):
    throttle_classes = [Throttle]

    @staticmethod
    def init_user(email, user_name, max_size):
        return User(user_name, email, max_size)

    def get(self, request):
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            return JsonResponse(
                {"error": f"Invalid page number {request.GET.get('page')}"}, status=400
            )

        user = self.init_user(request.auth_user.email, request.auth_user.user_name, 10)
        data = user.user_data(page=page)
        response = data if data else dict(detail="No data found!")
        return JsonResponse(response, status=200, safe=False)
