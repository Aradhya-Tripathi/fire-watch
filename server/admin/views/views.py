from admin import admin_model
from apis.views import JsonResponse, request
from apis.views.decorators import api_view


@api_view(["GET"])
def admin_view(request: request):
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        return JsonResponse(data={"error": "Invalid page number"}, status=400)
    details = admin_model.get_unit_details(page=page)
    return JsonResponse(data={"data": details}, status=200)
