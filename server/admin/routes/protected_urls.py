from admin.routes import path
from admin.views import views

urlpatterns = [path("details", views.AdminView.as_view())]
