from django.urls import include, path
from rest_framework import routers
from api.viewsets import DeviceViewSet,VulnerabilityViewSet,PrivacyInformationViewSet

router = routers.DefaultRouter()



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('devices/', DeviceViewSet.as_view()),
    path('vulnerability/', VulnerabilityViewSet.as_view()),    
    path('privacy/', PrivacyInformationViewSet.as_view()),    
]