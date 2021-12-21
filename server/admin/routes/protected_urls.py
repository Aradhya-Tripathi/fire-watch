from admin.routes import path
from admin.views import views

urlpatterns = [path("", views.AdminView.as_view())]
