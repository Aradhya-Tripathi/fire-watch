from authentication.views import Login, ResetPassword
from django.urls import path

from .views import Alert, CollectData, ProtectedView, Register

urlpatterns = [
    path("register", Register.as_view()),
    path("login", Login.as_view()),
    path("protected", ProtectedView.as_view()),
    path("upload", CollectData.as_view()),
    path("reset-password", ResetPassword.as_view()),
    path("sos", Alert.as_view()),
]
