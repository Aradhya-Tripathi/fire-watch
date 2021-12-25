from authentication.routes import path
from authentication.views import views

urlpatterns = [
    path("login", views.Login.as_view()),
    path("reset-password", views.ResetPassword.as_view()),
    path("refresh", views.RefreshToAccess.as_view()),
]
