from apis.views import JsonResponse, Throttle
from apis.views.decorators import api_view


@api_view(["GET"], [Throttle])
def protected(request):
    return JsonResponse(data={"Success": True}, status=200)
