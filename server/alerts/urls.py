from django.urls import path
from .views import Alert, NotFound

urlpatterns = [
    path("alerts", Alert.as_asgi()),
    path("not-found", NotFound.as_asgi()),
]
