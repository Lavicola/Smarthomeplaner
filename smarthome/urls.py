from django.urls import path,include
from django.views.generic import TemplateView

from . import views
app_name = "smarthome"
urlpatterns = [
    path('devices/<str:device_name>/', views.device_overview, name='device'),
    path('devices/', views.devices_overview, name='devices'),
]
