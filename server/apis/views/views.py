import json
from typing import Dict, Union

import fire_watch
from alerts import email_service
from apis.views import BaseAPIView, HttpRequest, JsonResponse
from apis.views.decorators import api_view
from asgiref.sync import async_to_sync
from authentication import permissions, utils
from channels.layers import get_channel_layer
from fire_watch.log.log_configs import get_logger

from ..definitions import UserSchema
from ..transactions import enter_user, insert_data
from ..utils import check_subscription


@api_view(["POST"])
def register(request: HttpRequest) -> JsonResponse:
    """Register users

    Args:
        request (request): wsgi request

    Returns:
        JsonResponse: Response
    """
    validate = UserSchema(data=request.data, register=True).approval()

    if "error" in validate:
        return JsonResponse(data={"error": validate["error"]}, status=400)

    enter_user(validate)
    return JsonResponse(data={"success": True}, status=201)


@api_view(["POST"], permission_classes=[permissions.ValidateUnit])
def collect_data(request: HttpRequest) -> JsonResponse:
    """Accept data dumps from device

    Args:
        request (request): wsgi request

    Returns:
        JsonResponse: Response
    """
    validate = UserSchema(data=request.data, upload=True).approval()
    if "error" in validate:
        return JsonResponse(data={"error": validate["error"]}, status=400)

    insert_data(unit_id=request.unit_id, data=request.data)
    return JsonResponse({}, status=201)


class Alert(BaseAPIView):
    permission_classes = [permissions.ValidateUnit]
    group_name = fire_watch.conf.socket["base_group"]
    channel_layer = get_channel_layer()

    logger = get_logger(__name__, filename="./alerts.log")

    def send_alert(
        self, token: str, data: Dict[str, Union[str, int]], to: str = None
    ) -> None:
        """Send alert to group.
           Get group id -> common `group_name` + `unit_id`
           send alert to that group

        Args:
            token (str): unit_id
            data (Dict[str, Union[str, int]]): alert data

        Returns:
            None
        """
        subs = check_subscription()
        if "email" in subs:
            email_service.send_mail(html="[Place Holder]", subject="Alert", to=[to])
        if "ws" in subs:
            group_id = self.group_name + str(token)
            async_to_sync(self.channel_layer.group_send)(
                group_id, {"type": "send.alert", "content": data}
            )

    def post(self, request: HttpRequest) -> JsonResponse:
        """Accept alert from device

        Args:
            request (request): wsgi request

        Returns:
            JsonResponse: Response
        """
        token = utils.get_token(request.headers)
        self.logger.warning(f"Alert {json.dumps(request.data)}")
        self.send_alert(token, request.data, to=request.email)
        return JsonResponse(data={}, status=200)
