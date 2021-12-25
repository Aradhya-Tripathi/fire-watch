from apis.views import protected_views
from apis.routes import path

urlpatterns = [
    path("test-protected", protected_views.test_protected),
    path("details", protected_views.UserAPI.as_view()),
]
