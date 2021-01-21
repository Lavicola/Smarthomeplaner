from rest_framework import serializers
from configurator.models import Device, Firmware




class FirmwareSerializer(serializers.ModelSerializer ):

    class Meta:
        model = Firmware
        fields = ('version_number','changelog','releasedate')
        #exclude = ('changelog_en','changelog_de')

 
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Firmware.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """

        return instance


class DeviceSerializer(serializers.ModelSerializer ):
    firmware_set = FirmwareSerializer(many=True)

    class Meta:
        model = Device
        #fields = '__all__' 
        fields=('name','image','manufacturer_name','generation','firmware_set')


