from rest_framework import viewsets, filters
from smarthome.models import Device,Firmware,Vulnerability,PrivacyInformation
from .serializers import DeviceSerializer,FirmwareSerializer,VulnerabilitySerializer,PrivacyInformationerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters  
from django.db.models import Q


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DeviceSerializer
    def get_queryset(self):
        queryset = Device.objects.all()
        device_name = self.request.query_params.get("name",None)
        device_category = self.request.query_params.get("category",None)
        if device_name is not None and device_category is not None:
            #print("device_name is not None and device_category is not None")
            criteria1 = Q(name__icontains=device_name)
            criteria2 = Q(category=device_category)
            queryset = queryset.filter(criteria1 & criteria2)
        elif device_name is not None:
            #print("device_name is not None")
            criteria1 = Q(name__icontains=device_name)
            queryset = queryset.filter(criteria1)
        return queryset




class FirmwareViewSet(viewsets.ModelViewSet):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer


class VulnerabilityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VulnerabilitySerializer
    def get_queryset(self):
        queryset = Vulnerability.objects.all()
        device_id = self.request.query_params.get("device_id",None)
        if device_id is not None:
            queryset = queryset.filter(device_id=device_id,patch_date__isnull = True)            
        return queryset

class PrivacyInformationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PrivacyInformationerializer
    def get_queryset(self):
        queryset = PrivacyInformation.objects.all()
        device_id = self.request.query_params.get("device_id",None)
        if device_id is not None:
            criteria1 = Q(device_id=device_id)
            queryset = queryset.filter(criteria1)
        return queryset


