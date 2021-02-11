from django.urls import include, path
from rest_framework import routers
from api.viewsets import DeviceViewSet,VulnerabilityViewSet,PrivacyIssueViewSet


router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet,basename="api")
router.register(r'vulnerability',VulnerabilityViewSet,basename="api")
router.register(r'privacy',PrivacyIssueViewSet,basename="api")



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]