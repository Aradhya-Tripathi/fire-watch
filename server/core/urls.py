
from django.urls import path
from django.urls import include

urlpatterns = [
    path('apis/', include('apis.urls'))
]
