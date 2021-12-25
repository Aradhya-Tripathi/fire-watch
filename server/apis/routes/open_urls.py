from apis.routes import path
from apis.views import views

urlpatterns = [
    path("register", views.register),
    path("upload", views.collect_data),
    path("sos", views.Alert.as_view()),
]
