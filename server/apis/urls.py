from django.urls import path
from .views import HealthCheck, Register

urlpatterns = [
    path('healthcheck', HealthCheck.as_view()),
    path('register', Register.as_view())
]