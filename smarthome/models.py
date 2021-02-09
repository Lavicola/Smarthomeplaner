from django.db import models
from django.utils.translation import gettext_lazy as _ #translation
from users.models import AbstractBaseUser
from django.contrib.auth import settings
from users.models import CustomUser

# Create your models here.


class Connector(models.Model):
    connector = models.CharField(max_length=30,primary_key=True )

    def __str__(self):
        return self.connector

    @staticmethod
    def GetConnector(a_connector_name):
        return Connector.objects.get(pk=a_connector_name)




class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to='Device')
    connector = models.ManyToManyField(Connector)
    release_date = models.DateField()
    manufacturer = models.CharField(max_length=200) 
    generation = models.CharField(max_length=10)

    class Device_Category(models.TextChoices):
        SMART_LIGHTING = "SL", _("SMART_LIGHTING")
        SMART_LOCK = "SLO" , _("SMART_LOCK")
        SMART_METERING_WATER = "SMW", _("SMART_METERING_WATER")
        SMART_METERING_ELECTRICITY ="SME", _("SMART_METERING_ELECTRICITY")
        SMAERT_METERING_WARMTH ="SMWA", _("SMAERT_METERING_WARMTH")
        VIRTUAL_ASSISTANT = "VA", _("VIRTUAL_ASSISTANT")
        SMART_THERMOSTAT = "ST", _("SMART_THERMOSTAT")
        SMART_CAM = "SC", _("SMART_CAM")
        SMART_SECURITY_SYSTEM = "SSS", _("SMART_SECURITY_SYSTEM")
    
    category = models.CharField(
        max_length=4,
        choices=Device_Category.choices
    )

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Device")
        constraints = [models.UniqueConstraint(fields=["name","manufacturer","generation"],name="unique_device")]

    def __str__(self):
        return self.name +" " + self.manufacturer + "  V" + self.generation


    @staticmethod
    def GetDevice(device_id):
        return Device.objects.filter(id=device_id).first()


class Firmware(models.Model):
    firmware_id = models.AutoField(primary_key=True) #todo rename to id
    compatibility_list = models.ManyToManyField(Device,verbose_name= _("Firmware Compatible with"))
    version_number = models.CharField(max_length=50,verbose_name= _("Versionnumber"))
    changelog = models.CharField(verbose_name=_("Changelog"), max_length=500)
    release_date = models.DateField(verbose_name=_("Release Date"))

    class Meta:
        verbose_name = _("Firmware")
        verbose_name_plural = _("Firmwares")

    def __str__(self):
        firmwares = self.compatibility_list.all()
        manufacture = list(firmwares)[0].manufacturer
        return manufacture + " Version: "+ str(self.firmware_id)



class Vulnerability(models.Model):
    device_id = models.ManyToManyField(Device,verbose_name= _("Vulnerability exploitable by:"))
    description = models.CharField(max_length=500,verbose_name= _("Description of the Vulnerability "))
    paper_url = models.URLField(max_length=500,verbose_name= _("URL to the Article to the Vulnerability"))
    patch_date = models.DateField(verbose_name= _("Vulnerability was patched on:"),blank=True)
    url_patch = models.URLField(max_length=500,verbose_name= _("URL to the Patch Article"),blank=True)


    class Vulnerability_Category(models.TextChoices):
        Firmware = "Firmware", _("Firmware")
        Physical = "Physical" , _("Physical")
        Others = "Others", _("Others")

    category = models.CharField(max_length=8,choices=Vulnerability_Category.choices)

    class Meta:
        verbose_name = _("Vulnerability")
        verbose_name_plural = _("Vulnerabilities")

    def __str__(self):
        return str(self.description) 



class DeviceEntry(models.Model):
    id = models.AutoField(primary_key=True)
    unique_room = models.ForeignKey("Room",on_delete=models.CASCADE)
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    connector = models.ForeignKey(Connector,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["unique_room","device","connector","quantity"],name="unique_entry")]


    def __str__(self):
        return self.device.manufacturer +" "+ self.device.name +" "+ str(self.quantity) 


#
# device_list list of dict with {device_id,connector}
#

    @staticmethod
    def setEntries(a_room,device_list_dict):
        # get list of device_ids
        print(device_list_dict)
        device_list = [a_dict["device_id"] for a_dict in device_list_dict]

        # get the unique connectors
        unique_dict_list = list(map(dict, set(tuple(sorted(sub.items())) for sub in device_list_dict))) 
        unique_connector_list = [a_dict["connector"] for a_dict in unique_dict_list]

        for id in set(device_list):
            device_object = Device.GetDevice(id)
            for connector in unique_connector_list:                
                quantity = DeviceEntry.GetDeviceQuantity(device_list_dict,id,connector)
                if(quantity == 0):
                    continue
                else:
                    if(DeviceEntry.exists(a_room,device_object,connector)):
                        DeviceEntry.UpdateQuantity(a_room,device_object,Connector.GetConnector(connector),quantity)
                    else:
                        DeviceEntry.setEntry(a_room,device_object,Connector.GetConnector(connector),quantity)

        return 


    @staticmethod
    def DeleteUnusedEntries(a_room,device_list_dict):
        device_entries = DeviceEntry.objects.filter(unique_room=a_room)
        unique_dict_list = list(map(dict, set(tuple(sorted(sub.items())) for sub in device_list_dict))) 
        found = False
        for entry in device_entries:
            for dict_entry in unique_dict_list:
                if(dict_entry["connector"] == entry.connector.connector and int(dict_entry["device_id"]) == entry.device.id):
                    found=True
                else:
                    continue
            if not (found):
                DeviceEntry.delete(entry)
            found = False




            





        return 

    @staticmethod
    def GetDeviceQuantity(device_list_dict, a_device_id,a_connector):
        quantity = len([i for i in device_list_dict if i['connector'] == a_connector and i["device_id"] == a_device_id ])
        return quantity


    @staticmethod
    def setEntry(room,device,a_connector,a_quantity):
        DeviceEntry.save(DeviceEntry(unique_room=room,device=device,connector=a_connector,quantity=a_quantity))
        return True

    @staticmethod
    def UpdateQuantity(a_room,a_device,a_connector,a_quantity):
        DeviceEntry.objects.filter(unique_room=a_room,device=a_device,connector=a_connector).update(quantity=a_quantity)
        return True

    @staticmethod
    def DeleteEntry(a_room,a_device,a_connector):
        DeviceEntry.objects.get(unique_room=a_room,connector=a_connector,device=a_device).delete()
        return 

    # gives the current Device Entry quantity which is saved in the database back. 
    @staticmethod
    def GetCurrentDeviceQuantity(a_room,a_device):
        return DeviceEntry.objects.only("quantity").get(unique_room=a_room,device=a_device).quantity


    @staticmethod
    def exists(a_room,a_device,a_connector):
        if( DeviceEntry.objects.filter(unique_room=a_room,device=a_device,connector=a_connector).count() == 0 ):
            return False
        return True




class Room(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    room_name = models.CharField(max_length=50)


    class Meta:
        constraints = [models.UniqueConstraint(fields=["user","room_name"],name="unique_room")]


    def __str__(self):
        return self.room_name  


    @staticmethod
    def GetExistingRoomNames(a_email):
        room_names = []
        for room in Room.objects.raw('SELECT DISTINCT room_name,id FROM `smarthome_room` WHERE `user_id` = %s;',[a_email]):
            room_names.append(room.room_name)
        return room_names


    @staticmethod
    def DeleteUnusedRooms(a_email,a_room_names):
        current_room_names = Room.GetExistingRoomNames(a_email)

        for name in current_room_names:
            if name not in a_room_names:
                Room.delete(a_email,name)

        return 


    @staticmethod
    def GetRoom(a_email,a_room_name):
                
        return Room.objects.filter(user=a_email,room_name=a_room_name).first()


    @staticmethod
    def exists(a_email,a_room_name):

        return Room.objects.filter(user=a_email,room_name=a_room_name).exists()


    @staticmethod
    def create(a_email,a_name):

        Room.save(Room(user_id=a_email,room_name=a_name))

        return True
    
    @staticmethod
    def CreateRooms(a_email,a_names):
        
        for name in a_names:
            if(Room.exists(a_email,name) == False):
                Room.create(a_email,name)
        return True

    @staticmethod
    def DeleteRooms(a_email,a_names):
        
        for name in names:
            Room.delete(a_email,a_names)

        return True


    @staticmethod
    def delete(a_email,a_names):
        
        Room.objects.filter(user_id=a_email,room_name=a_names).delete()
        return True





    














    
from smarthome.signals import *

    






"""




class App(models.Model):
    name = models.CharField(primary_key=True,max_length=60)
    manufacturer = models.CharField(max_length=200)
    functionality = models.CharField(max_length=1000)
    releasedate = models.CharField(max_length=20)



class AppUpdate(models.Model):
    version_number = models.CharField(primary_key=True,max_length=50)
    releasedate = models.CharField(max_length=20) 
    changelog = models.CharField(max_length=200)

class DataProtection(models.Model):
    discovery = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    
"""










