from rest_framework import serializers
from smarthome.models import Device, Firmware,Vulnerability,PrivacyInformation,Category,Connector
from configurator.models import CanvasMap




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
    #firmware_set = FirmwareSerializer(many=True)
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
    device_id = DeviceSerializerShort(many = True)

    class Meta:
        model = Vulnerability
        fields=("device_id",'discovery',"description","paper_url","patch_date","url_patch")


class PrivacyInformationerializer(serializers.ModelSerializer ):
    device_id = DeviceSerializerShort(many=True)

    class Meta:
        model = PrivacyInformation
        fields=("device_id","description","paper_url")



