from django.urls import include, path
from rest_framework import routers
from api.views import DeviceViewSet


router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet,basename="api")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]