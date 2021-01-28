from django.urls import path,include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('setCanvas',views.setCanvas,name='setCanvas'),
    path('getCanvas',views.getCanvas,name='getCanvas'),
    path('saveRooms',views.saveRooms,name='saveRooms'),

]
