from django.urls import path
from .views import Alert

urlpatterns = [path("alerts", Alert.as_asgi())]