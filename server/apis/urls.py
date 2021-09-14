from django.urls import path
from .views import SOS, HealthCheck, Register, Login, ProtectedView, CollectData

urlpatterns = [
    path("healthcheck", HealthCheck.as_view()),
    path("register", Register.as_view()),
    path("login", Login.as_view()),
    path("protected", ProtectedView.as_view()),
    path("upload", CollectData.as_view()),
    path("sos", SOS.as_view())
]
