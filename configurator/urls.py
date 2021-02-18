from django.urls import path,include
from django.views.generic import TemplateView

from . import views
app_name = "configurator"
urlpatterns = [
    path('', views.index, name='index'),
    path('getCanvas',views.getCanvas,name='getCanvas'),
    path('saveConfiguration',views.saveConfiguration,name='saveConfiguration'),
    path('configuration',views.configuration,name='smarthome_configurator'),
]
