from rest_framework import routers
from .viewsets import DeviceViewSet,FirmwareViewSet

router = routers.DefaultRouter()
router.register(r'device', DeviceViewSet,basename="device")
router.register(r'firmware', FirmwareViewSet)