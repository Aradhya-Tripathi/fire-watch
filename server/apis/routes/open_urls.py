from apis.routes import path
from apis.views import views
from authentication import views as auth_views

urlpatterns = [
    path("register", views.Register.as_view()),
    path("login", auth_views.Login.as_view()),
    path("upload", views.CollectData.as_view()),
    path("reset-password", auth_views.ResetPassword.as_view()),
    path("sos", views.Alert.as_view()),
]
