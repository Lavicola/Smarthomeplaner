from django.urls import path,include
from .routers import router
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('configurator/<int:device_id>/', views.device_detail, name='device_detail'),
    path('firmware_list', views.firmware_list, name='firmware_list'),
    path('device', TemplateView.as_view(template_name='index.html')),
    path('setCanvas',views.setCanvas,name='setCanvas'),
    path('getCanvas',views.getCanvas,name='getCanvas'),

    path(r'api/',include(router.urls))
]
