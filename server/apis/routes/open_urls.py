from apis.routes import path
from apis.views import views
from authentication.views import views as auth_views

urlpatterns = [
    path("register", views.register),
    path("login", auth_views.Login.as_view()),
    path("upload", views.collect_data),
    path("reset-password", auth_views.ResetPassword.as_view()),
    path("sos", views.Alert.as_view()),
]
