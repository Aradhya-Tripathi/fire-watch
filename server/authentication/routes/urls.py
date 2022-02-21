from authentication.routes import path
from authentication.views import views

urlpatterns = [
    path("login", views.login_users),
    path("reset-password", views.reset_password),
    path("refresh", views.refresh_to_acess),
    path("logout", views.logut_users),
]
