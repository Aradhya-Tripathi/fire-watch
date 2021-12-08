from django.urls import include, path

from .views import HealthCheck

urlpatterns = [
    path("apis/", include("apis.urls")),
    path("health-check", HealthCheck.as_view()),
]
