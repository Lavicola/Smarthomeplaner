from django.urls import path,include
from django.views.generic import TemplateView

from . import views
app_name = "configurator"
urlpatterns = [
    path('', views.index, name='index'),
    path('setCanvas',views.setCanvas,name='setCanvas'),
    path('getCanvas',views.getCanvas,name='getCanvas'),
    path('saveRooms',views.saveRooms,name='saveRooms'),
    path('configuration',views.congifuration,name='configuration'),


]
