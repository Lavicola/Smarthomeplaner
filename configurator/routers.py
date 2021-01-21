from rest_framework import routers
from .viewsets import DeviceViewSet,FirmwareViewSet

router = routers.DefaultRouter()
router.register(r'device', DeviceViewSet)
router.register(r'firmware', FirmwareViewSet)