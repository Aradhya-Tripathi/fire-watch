import os

from alerts.urls import urlpatterns
from authentication.socket_middleware import AuthMiddleWare
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fire_watch.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddleWare(AuthMiddlewareStack(URLRouter(urlpatterns))),
    }
)
