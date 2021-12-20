from admin.routes import path
from admin.views import views

urlpatterns = [path("", views.admin_view)]
