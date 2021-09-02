from django.urls import path
from .views import HealthCheck

urlpatterns = [
    path('healthcheck', HealthCheck.as_view())
]