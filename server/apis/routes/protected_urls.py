from apis.views import protected_views
from apis.routes import path

urlpatterns = [
    path("me", protected_views.me),
    path("details", protected_views.UserAPI.as_view()),
]
