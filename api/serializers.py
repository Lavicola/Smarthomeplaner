from rest_framework import serializers
from smarthome.models import Device, Firmware,Vulnerability,DataProtectionInformation,Connector
from configurator.models import CanvasMap



# not used but could be used in the future-
class FirmwareSerializer(serializers.ModelSerializer ):

    class Meta:
        model = Firmware
        fields = ('version_number','changelog')



class ConnectorSerializer(serializers.ModelSerializer ):
    class Meta:
        model = Connector
        #fields = '__all__' 
        fields=('connector',)



class DeviceSerializer(serializers.ModelSerializer ):
    connector = ConnectorSerializer(many=True)
    class Meta:
        model = Device
        #fields = '__all__' 
        fields=('id','name','image','manufacturer','connector','generation','category')



class DeviceSerializerShort(serializers.ModelSerializer ):
    class Meta:
        model = Device
        #fields = '__all__' 
        fields=('name',)



class VulnerabilitySerializer(serializers.ModelSerializer ):
    #many = true means we have a many to many relationship
    device_id = DeviceSerializerShort(many = True)

    class Meta:
        model = Vulnerability
        fields=("device_id",'discovery',"description","paper_url")


class DataProtectionInformationerializer(serializers.ModelSerializer ):
    device_id = DeviceSerializerShort(many=True)

    class Meta:
        model = DataProtectionInformation
        fields=("device_id","description","paper_url")



