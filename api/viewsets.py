from rest_framework import viewsets, filters
from smarthome.models import Device,Firmware,Vulnerability,PrivacyIssue,Category
from .serializers import DeviceSerializer,FirmwareSerializer,VulnerabilitySerializer,PrivacyIssueSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters  
from django.db.models import Q


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DeviceSerializer
    def get_queryset(self):
        queryset = Device.objects.all()
        device_name = self.request.query_params.get("name")
        device_category = self.request.query_params.get("category")

        if(device_name != ""):
            if(device_category != "all"):
                category_id = Category.objects.filter(category=device_category).get()
                criteria1 = Q(name__icontains=device_name)
                criteria2 = Q(category=category_id)
                queryset = queryset.filter(criteria1 & criteria2)
            else:
                criteria1 = Q(name__icontains=device_name)
                queryset = queryset.filter(criteria1)
        else:
             if(device_category != "all"):
                category_id = Category.objects.filter(category=device_category).get()                
                criteria1 = Q(category=category_id)
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
        #todo check if int?
        if device_id is not None:
            criteria1 = Q(device_id=device_id)
            queryset = queryset.filter(criteria1)
        return queryset



class VulnerabilityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VulnerabilitySerializer
    def get_queryset(self):
        queryset = Vulnerability.objects.all()
        device_id = self.request.query_params.get("device_id",None)
        #todo check if int?
        if device_id is not None:
            criteria1 = Q(device_id=device_id)
            queryset = queryset.filter(criteria1)
        return queryset

class PrivacyIssueViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PrivacyIssueSerializer
    def get_queryset(self):
        queryset = PrivacyIssue.objects.all()
        device_id = self.request.query_params.get("device_id",None)
        #todo check if int?
        if device_id is not None:
            criteria1 = Q(device_id=device_id)
            queryset = queryset.filter(criteria1)
        return queryset


