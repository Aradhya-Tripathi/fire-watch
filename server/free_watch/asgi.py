"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from authentication.socket_middleware import AuthMiddleWare
from alerts.urls import urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "free_watch.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddleWare(AuthMiddlewareStack(URLRouter(urlpatterns))),
    }
)
