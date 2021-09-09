from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class test(JsonWebsocketConsumer):
    group_name = "Alert"

    def connect(self):
        if isinstance(self.scope.get("error"), str):
            self.close()
            return

        self.accept()
        self.add_to_group()

    def add_to_group(self):
        channel_layer = get_channel_layer()
        self.group_id = self.group_name + str(self.scope["current"]["exp"])
        print(self.group_id)
        async_to_sync(channel_layer.group_add)(self.group_id, self.channel_name)

    def disconnect(self, code):
        super().disconnect(code)
