from django.urls import path,include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('firmware_list', views.firmware_list, name='firmware_list'),
    path('device', TemplateView.as_view(template_name='index.html')),
]
