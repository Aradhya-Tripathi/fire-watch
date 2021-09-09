from django.urls import path
from .views import test

urlpatterns = [path("alerts", test.as_asgi())]