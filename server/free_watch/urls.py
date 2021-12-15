from django.urls import include, path

from .views import health_check

urlpatterns = [
    path("apis/", include("apis.urls")),
    path("health-check", health_check),
]
