from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from core.errorfactory import SocketAuthenticationFailed
from .checks import authenticate
from core import conf


GROUP_NAME = conf["socket"]["base_group"]


class Alert(JsonWebsocketConsumer):
    def connect(self):
        try:
            authenticate(scope=self.scope)
        except SocketAuthenticationFailed:
            self.close()
            return

        self.accept()
        self.channel_layer = get_channel_layer()
        self.add_to_group()

    def send_alert(self, content):
        self.send_json(content["content"])

    def add_to_group(self):
        """Add users to specified group, using `channel_name`
        as the unique user identifier.
        """
        self.group_id = GROUP_NAME + str(self.scope["unit_id"])
        async_to_sync(self.channel_layer.group_add)(self.group_id, self.channel_name)

    def disconnect(self, code):
        super().disconnect(code)


class NotFound(JsonWebsocketConsumer):
    def connect(self):
        self.close()
