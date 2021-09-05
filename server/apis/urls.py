from django.urls import path
from .views import HealthCheck, Register, Login

urlpatterns = [
    path("healthcheck", HealthCheck.as_view()),
    path("register", Register.as_view()),
    path("login", Login.as_view()),
]
