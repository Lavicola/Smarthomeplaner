from rest_framework import viewsets, filters
from .models import Device,Firmware
from .serializers import DeviceSerializer,FirmwareSerializer
from rest_framework.response import Response


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    search_fields = ('name')



class FirmwareViewSet(viewsets.ModelViewSet):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
