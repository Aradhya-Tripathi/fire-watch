import json
from typing import Dict, Union

from asgiref.sync import async_to_sync
from authentication import permissions, utils
from channels.layers import get_channel_layer
from core import conf
from core.log.log_configs import get_logger
from core.throttle import Throttle
from django.http import request
from django.http.response import JsonResponse
from rest_framework.views import APIView

from .checks import enter_user, insert_data
from .definitions import UserSchema
from .utils import check_subscription


class Register(APIView):
    throttle_classes = [Throttle]

    def post(self, request: request, **kwargs) -> JsonResponse:
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


class CollectData(APIView):
    permission_classes = [permissions.ValidateUnit]
    throttle_classes = [Throttle]

    def post(self, request: request, **kwargs) -> JsonResponse:
        """Accept data dumps from device

        Args:
            request (request): wsgi request

        Returns:
            JsonResponse: Response
        """
        insert_data(unit_id=request.unit_id, data=request.data)
        return JsonResponse({}, status=201)


class Alert(APIView):
    permission_classes = [permissions.ValidateUnit]
    group_name = conf["socket"]["base_group"]
    channel_layer = get_channel_layer()

    logger = get_logger(__name__, filename="./alerts.log")

    def send_alert(self, token: str, data: Dict[str, Union[str, int]]) -> None:
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
            # TODO: Include email
            ...
        if "ws" in subs:
            group_id = self.group_name + str(token)
            async_to_sync(self.channel_layer.group_send)(
                group_id, {"type": "send.alert", "content": data}
            )

    def post(self, request: request, **kwargs) -> JsonResponse:
        """Accept alert from device

        Args:
            request (request): wsgi request

        Returns:
            JsonResponse: Response
        """

        token = utils.get_token(request.headers)
        self.logger.warning(f"Alert {json.dumps(request.data)}")
        self.send_alert(token, request.data)
        return JsonResponse(data={}, status=200)


class ProtectedView(APIView):
    throttle_classes = [Throttle]

    def get(self, request: request, **kwargs) -> JsonResponse:
        """Test protected route

        Args:
            request (request): request object

        Returns:
            JsonResponse: Response
        """
        return JsonResponse(data={"success": True}, status=200)
