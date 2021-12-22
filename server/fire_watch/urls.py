from django.urls import include, path

from .views import health_check

urlpatterns = [
    path("", include("apis.routes.open_urls")),
    path("health-check", health_check),
    path("user/", include("apis.routes.protected_urls")),
    path("admin/", include("admin.routes.protected_urls")),
]
