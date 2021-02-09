from django.urls import path,include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:device_id>/', views.detail, name='detail'),
]
