from rest_framework import serializers
from smarthome.models import Device, Firmware,Vulnerability,PrivacyIssue
from configurator.models import CanvasMap




class FirmwareSerializer(serializers.ModelSerializer ):

    class Meta:
        model = Firmware
        fields = ('version_number','changelog','releasedate')



class DeviceSerializer(serializers.ModelSerializer ):
    firmware_set = FirmwareSerializer(many=True)

    class Meta:
        model = Device
        #fields = '__all__' 
        fields=('id','name','image','category','manufacturer','connector','generation','firmware_set')


class DeviceSerializerShort(serializers.ModelSerializer ):
    
    class Meta:
        model = Device
        #fields = '__all__' 
        fields=('name',)



class VulnerabilitySerializer(serializers.ModelSerializer ):
    device_id = DeviceSerializerShort(many=True)

    class Meta:
        model = Vulnerability
        fields=("device_id",'discovery',"description","paper_url","patch_date","url_patch")


class PrivacyIssueSerializer(serializers.ModelSerializer ):
    device_id = DeviceSerializerShort(many=True)

    class Meta:
        model = Vulnerability
        fields=("device_id",'discovery',"description","paper_url","patch_date","url_patch")



