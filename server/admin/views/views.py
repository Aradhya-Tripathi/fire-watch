from datetime import timedelta

from admin import admin_model
from apis.definitions import AdminSchema
from apis.views import BaseAPIView, JsonResponse, request
from authentication import issue_keys
from authentication.utils import admin_login


class AdminView(BaseAPIView):
    def get(request: request) -> JsonResponse:
        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            return JsonResponse(data={"error": "Invalid page number"}, status=400)
        details = admin_model.get_unit_details(page=page)
        return JsonResponse(data={"data": details}, status=200)

    def post(request: request) -> JsonResponse:
        validate = AdminSchema(request.data)
        if "error" in validate:
            return JsonResponse(data={"error": validate["error"]}, status=400)
        creds = admin_login(validate["password"], validate["email"])
        payload = {"email": creds["email"]}
        key = issue_keys.generate_key(
            payload=payload,
            expiry=timedelta(hours=1),
            get_refresh=True,
            refresh_exipry=timedelta(hours=12),
            is_admin=True,
        )
        return JsonResponse(
            data={
                "access_token": key["access_token"],
                "refresh_token": key["refresh_token"],
            },
            status=200,
        )
