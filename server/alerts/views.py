from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Alert(JsonWebsocketConsumer):
    group_name = "Alert"

    def connect(self):
        if "error" in self.scope:
            self.close()
            return None

        self.accept()
        self.channel_layer = get_channel_layer()
        self.add_to_group()

    def send_alert(self, content):
        self.send_json(content["content"])

    def add_to_group(self):
        self.group_id = self.group_name + str(self.scope["current"])
        async_to_sync(self.channel_layer.group_add)(self.group_id, self.channel_name)

    def disconnect(self, code):
        super().disconnect(code)
