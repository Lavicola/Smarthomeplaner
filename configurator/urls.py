from django.urls import path,include
from .routers import router
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.devices_overview, name='devices'),
    path('configurator/<int:device_id>/', views.device_detail, name='device_detail'),
    path('acdc', views.acdc, name='acdc'),
    path('firmware_list', views.firmware_list, name='firmware_list'),
    path('device', TemplateView.as_view(template_name='index.html')),
    path(r'api/',include(router.urls))
]