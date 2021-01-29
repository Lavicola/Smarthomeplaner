from django.db import models
from django.utils.translation import gettext_lazy as _ #translation
from users.models import AbstractBaseUser
from django.contrib.auth import settings
from users.models import CustomUser

# Create your models here.

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to='Device')
    release_date = models.DateField()
    manufacturer_name = models.CharField(max_length=200)
    connector = models.CharField(max_length=20)
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
        verbose_name = _("Gerät")
        verbose_name_plural = _("Geräte")
        constraints = [models.UniqueConstraint(fields=["name","manufacturer_name","generation"],name="unique_device")]

    def __str__(self):
        return self.name +" " + self.manufacturer_name + "  V" + self.generation


    @staticmethod
    def GetDevice(device_id):


        return Device.objects.filter(id=device_id).first()



class Interface(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    connector = models.CharField(max_length=30)


class Firmware(models.Model):
    firmware_id = models.AutoField(primary_key=True)
    compatibility_list = models.ManyToManyField(Device,verbose_name= _("Firmware Kompatibel mit"))
    version_number = models.CharField(max_length=50,verbose_name= _("Versionsnummer"))
    changelog = models.CharField(verbose_name=_("Änderungen"), max_length=500)
    release_date = models.DateField(verbose_name=_("Erscheinungsdatum"))

    class Meta:
        verbose_name = _("Firmware")
        verbose_name_plural = _("Firmwares")



class Vulnerability(models.Model):
    device_id = models.ManyToManyField(Device,verbose_name= _("Schwachstelle bei folgenden Geräten ausnutzbar:"))
    discovered_date = models.DateField(verbose_name= _("Schwachstelle wurde gefunden am:"))
    description = models.CharField(max_length=300,verbose_name= _("Beschreibung der Schwachstelle"))
    url = models.URLField(max_length=200,verbose_name= _("URL zum Artikel der Schwachstelle"))
    category = models.CharField(max_length=20,verbose_name= _("Kategorie"))
    patch_date = models.DateField(verbose_name= _("Schwachstelle wurde gepatched am:"))
    url_patch = models.URLField(max_length=200,verbose_name= _("Link zum Artikel des Patches"))
    patched = models.BooleanField(default= False,verbose_name= _("Schwachstelle wurde behoben:"))

    class Meta:
        verbose_name = _("Schwachstelle")
        verbose_name_plural = _("Schwachstellen")

    def __str__(self):
        return str(self.description) 



class DeviceEntry(models.Model):
    id = models.AutoField(primary_key=True)
    unique_room = models.ForeignKey("Room",on_delete=models.CASCADE)
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["unique_room","device","quantity"],name="unique_entry")]


    def __str__(self):
        return self.device.manufacturer_name +" "+ self.device.name +" "+ str(self.quantity) 


    @staticmethod
    def setEntries(email,room_name,device_list):

        for id in set(device_list):
            room_object = Room.GetRoom(email,room_name)
            device_object = Device.GetDevice(id)
            quantity = DeviceEntry.GetDeviceQuantity(device_list,id)
            if(DeviceEntry.exists(room_object,device_object)):
                DeviceEntry.UpdateQuantity(room_object,device_object,quantity)
            else:
                DeviceEntry.setEntry(room_object,device_object,quantity)
            
        return 

    @staticmethod
    def setEntry(room,device,a_quantity):
        DeviceEntry.save(DeviceEntry(unique_room=room,device=device,quantity=a_quantity))
        return True

    @staticmethod
    def UpdateQuantity(a_room,a_device,a_quantity):
        DeviceEntry.objects.filter(unique_room=a_room,device=a_device).update(quantity=a_quantity)
        return True


    @staticmethod
    def GetDeviceQuantity(a_device_list, a_device_id):

        return a_device_list.count(a_device_id)

    # gives the current Device Entry quantity which is saved in the database back. 
    @staticmethod
    def GetCurrentDeviceQuantity(a_room,a_device):
        return DeviceEntry.objects.only("quantity").get(unique_room=a_room,device=a_device).quantity


    @staticmethod
    def exists(a_room,a_device):
        if( DeviceEntry.objects.filter(unique_room=a_room,device=a_device).count() == 0 ):
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
    manufacturer_name = models.CharField(max_length=200)
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










