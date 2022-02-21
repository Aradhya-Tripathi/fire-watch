from datetime import timedelta

import fire_watch
from apis.definitions import UserSchema
from apis.views import HttpRequest, JsonResponse, api_view
from authentication.definitions import logout_schema
from authentication.permissions import RefreshToAccessPermission
from authentication.utils import login
from authentication.utils import reset_password as reset

from .. import issue_keys


@api_view(["POST"])
def login_users(request: HttpRequest) -> JsonResponse:
    validate = UserSchema(data=request.data).approval()

    if "error" in validate:
        return JsonResponse(data={"error": validate["error"]}, status=400)

    creds = login(password=validate.get("password"), email=validate.get("email"))

    payload = {"user_name": creds["user_name"], "email": creds["email"]}
    key = issue_keys.generate_key(
        payload=payload,
        expiry=timedelta(hours=fire_watch.conf.token_expiration),
        get_refresh=True,
        refresh_expiry=timedelta(hours=fire_watch.conf.refresh_expiration),
        is_admin=False,
    )
    return JsonResponse(
        data={
            "access_token": key["access_token"],
            "refresh_token": key["refresh_token"],
        },
        status=200,
    )


@api_view(["POST"])
def reset_password(request: HttpRequest) -> JsonResponse:
    validate = UserSchema(data=request.data, reset=True).approval()
    if "error" in validate:
        return JsonResponse(data={"error": validate["error"]}, status=400)
    reset(request.data)
    return JsonResponse(data={}, status=200)


@api_view(["POST"], permission_classes=[RefreshToAccessPermission])
def refresh_to_acess(request: HttpRequest):
    tokens = issue_keys.refresh_to_access(request.refresh_token)
    fire_watch.cache.sadd("Blacklist", request.refresh_token)
    fire_watch.cache.expiremember(
        "Blacklist",
        request.refresh_token,
        issue_keys.valid_for(request.refresh_token).seconds,
    )
    return JsonResponse(data=tokens, status=200)


@api_view(["POST"])
def logut_users(request: HttpRequest):
    tokens = logout_schema(request.data)
    if not issue_keys.verify_key(
        tokens["access_token"]
    ) or not issue_keys.is_valid_refresh(tokens["refresh_token"]):
        return JsonResponse(data={"error": "Invalid tokens"}, status=401)

    fire_watch.cache.sadd("Blacklist", tokens["access_token"], tokens["refresh_token"])
    fire_watch.cache.expiremember(
        "Blacklist",
        tokens["access_token"],
        issue_keys.valid_for(key=tokens["access_token"]).seconds,
    )
    fire_watch.cache.expiremember(
        "Blacklist",
        tokens["refresh_token"],
        issue_keys.valid_for(key=tokens["refresh_token"]).seconds,
    )
    return JsonResponse(data={"success": True}, status=200)
