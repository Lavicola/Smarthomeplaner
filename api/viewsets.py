from smarthome.models import Connector
from rest_framework import viewsets, filters
from smarthome.models import Device,Firmware,Vulnerability,DataProtectionInformation
from .serializers import DeviceSerializer,FirmwareSerializer,VulnerabilitySerializer,DataProtectionInformationerializer
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
            criteria1 = Q(name__icontains=device_name)
            criteria2 = Q(category=device_category)
            queryset = queryset.filter(criteria1 & criteria2)
        elif device_name is not None:
            criteria1 = Q(name__icontains=device_name)
            queryset = queryset.filter(criteria1)
        serializer = DeviceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PUT API for the webservice try. NOT SECURE
    def put(self, request):

        connectors = []
        standards = []
        device_data = JSONParser().parse(request)
        
        #Easier to ask for forgiveness than permission
        #get all connectors and standards

        try:
            for connector in device_data["connector"]:                
                connectors.append(Connector.GetConnector((connector["connector"])))        
            for standard in device_data["standard"]:
                standards.append(standard)        
        except KeyError:
            pass



        device = Device(name=device_data["name"],manufacturer=device_data["manufacturer"],generation=device_data["generation"])
        device.image = '/Device/HUE_E27_yjzDXH7.svg'
        device.category = 'SMART_PLUG' # not possible to set
        device.save() # Many 2 Many can only be set once the device exists.       
        device.connector.set(connectors)
        #device.standard.set(standards)
        
        return Response(status=status.HTTP_200_OK)


class FirmwareViewSet(viewsets.ModelViewSet):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer


class VulnerabilityViewSet(APIView):
    serializer_class = VulnerabilitySerializer

    def get(self, request):
        '''
        GET Requst to get all (open) Vulnerabilities for a device  
        '''
        queryset = Vulnerability.objects.all()
        device_id = self.request.query_params.get("device_id",None)
        if device_id is not None:
            queryset = queryset.filter(device_id=device_id,patch_date__isnull = True)            
        serializer = VulnerabilitySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class DataProtectionInformationViewSet(APIView):
    serializer_class = DataProtectionInformationerializer

    def get(self, request):
        queryset = DataProtectionInformation.objects.all()
        device_id = self.request.query_params.get("device_id",None)
        if device_id is not None:
            queryset = queryset.filter(device_id=device_id)            
        serializer = DataProtectionInformationerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

