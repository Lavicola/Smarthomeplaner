from smarthome.models import Connector
from rest_framework import viewsets, filters
from smarthome.models import Device,Firmware,Vulnerability,PrivacyInformation
from .serializers import DeviceSerializer,FirmwareSerializer,VulnerabilitySerializer,PrivacyInformationerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import JSONParser 
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters  
from django.db.models import Q









class DeviceViewSet(APIView):


    def get(self, request):
        '''
        List every device, device with name LIKE,device with certain category or both. 
        '''
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
        serializer = DeviceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT API for the webservice try. NOT SECURE
    def put(self, request):

        '''
        List every device, device with name LIKE,device with certain category or both. 
        '''
        connectors = []
        standards = []
        device_data = JSONParser().parse(request)
        
        #Easier to ask for forgiveness than permission
        #get all connectors and standards

        try:
            for connector in device_data["connector"]:                
                connectors.append(Connector.GetConnector((connector["connector"])))        
            #get all standards
            for standard in device_data["standard"]:
                #GetStandard(standard)
                standards.append(standard)        
        except KeyError:
            pass

        device = Device(name=device_data["name"],manufacturer=device_data["manufacturer"],generation=device_data["generation"])
        device.category = "Smart_Lightning"
        device.image = '/Device/HUE_E27_yjzDXH7.svg'
        device.category = 'SMART'
        device.save()        
        device.connector.set(connectors)
        #device.standard.set(standards)
        
        return Response(status=status.HTTP_200_OK)









class DeviceViewSet2(viewsets.ViewSet):
    serializer_class = DeviceSerializer


    def list(self,request):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices)



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


