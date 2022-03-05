import json

import fire_watch
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer


class Alert(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = fire_watch.conf.socket["base_group"]
        self.max_log_size = 15
        self._use_json = True

    def requested_json(self):
        # Defaults to json
        for header in self.scope["headers"]:
            if header[0].decode() == "content-type":
                return False if header[1].decode() == "plain/text" else True
        return True

    def connect(self):
        if "error" in self.scope:
            self.close()
            return

        self._use_json = self.requested_json()
        self.accept()
        self.channel_layer = get_channel_layer()
        self.add_to_group()
        # Show tail (max-size 15) if requested format is plain/text
        # This is to simulate data log when requested through CLI
        if not self._use_json:
            initial_data = "\n".join(
                map(
                    lambda x: x.decode(),
                    fire_watch.cache.lrange(
                        self.scope["unit_id"], 0, self.max_log_size
                    ),
                )
            )

            self.send(initial_data)

    def show_current_logs(self, message):
        # Show all incoming logs when logs are requested through CLI.
        # Appending to previously sent data post handshake.
        # Maintaining a max of 15 data points in cache for each user
        if fire_watch.cache.llen(self.scope["unit_id"]) >= self.max_log_size:
            fire_watch.cache.lpop(self.scope["unit_id"])

        fire_watch.cache.rpush(self.scope["unit_id"], json.dumps(message["log"]))
        data = "\n".join(
            map(
                lambda x: x.decode(),
                fire_watch.cache.lrange(self.scope["unit_id"], -1, -1),
            )
        )
        self.send(data) if not self._use_json else self.send_json(json.loads(data))

    def send_alert(self, content):
        self.send_json(content["content"])

    def add_to_group(self):
        """Add users to specified group, using `channel_name`
        as the unique user identifier.
        """
        self.group_id = self.group_name + str(self.scope["unit_id"])
        async_to_sync(self.channel_layer.group_add)(self.group_id, self.channel_name)

    def disconnect(self, code):
        super().disconnect(code)


class NotFound(JsonWebsocketConsumer):
    def connect(self):
        self.close()
