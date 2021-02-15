from django.db import models
from django.utils.translation import gettext_lazy as _ #translation
from users.models import AbstractBaseUser
from django.contrib.auth import settings
from users.models import CustomUser
from django.utils import timezone
from django.db.models.signals import m2m_changed, post_delete, pre_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.template.loader import get_template,render_to_string
from django.template import Context
from django.core.mail import send_mass_mail



# Create your models here.


class Connector(models.Model):
    connector = models.CharField(max_length=30,primary_key=True )

    def __str__(self):
        return self.connector

    @staticmethod
    def GetConnector(a_connector_name):
        return Connector.objects.get(pk=a_connector_name)


class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category



class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to='Device')
    connector = models.ManyToManyField(Connector)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    release_date = models.DateField(null=True,blank=True)
    manufacturer = models.CharField(max_length=200) 
    generation = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
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
    release_date = models.DateField(verbose_name=_("Release Date"),blank=True,null=True)

    class Meta:
        verbose_name = _("Firmware")
        verbose_name_plural = _("Firmwares")

    def __str__(self):
        firmwares = self.compatibility_list.all()
        manufacture = list(firmwares)[0].manufacturer
        devices = Device.objects.filter(firmware=self.firmware_id)
        device_names = ""

        for device in devices:
            device_names+=  str(device) + "," 
        return "Firmware Hersteller:"+manufacture +" Version: "+str(self.firmware_id)+ " supported devices:" + device_names



class Vulnerability(models.Model):
    device_id = models.ManyToManyField(Device,verbose_name= _("Vulnerability exploitable by:"))
    discovery = models.DateField(verbose_name= _("Vulnerability was found on:"))
    description = models.CharField(max_length=500,verbose_name= _("Description of the Vulnerability "))
    paper_url = models.URLField(max_length=500,verbose_name= _("URL to the Article to the Vulnerability"))
    patch_date = models.DateField(verbose_name= _("Vulnerability was patched on:"),null=True,blank=True)
    url_patch = models.URLField(max_length=500,verbose_name= _("URL to the Patch Article"),blank=True)
    created     = models.DateTimeField(editable=False,blank=True,null=True)
    modified    = models.DateTimeField(editable=False,blank=True,null=True)


    class Vulnerability_Category(models.TextChoices):
        Firmware = "Firmware", _("Firmware")
        Physical = "Physical" , _("Physical")
        Others = "Others", _("Others")

    category = models.CharField(max_length=8,choices=Vulnerability_Category.choices)



    class Meta:
        verbose_name = _("Vulnerability")
        verbose_name_plural = _("Vulnerabilities")
    
    def __str__(self):
        return self.description 




@receiver(m2m_changed, sender=Vulnerability.device_id.through)
def notify_users(sender,action,pk_set,instance, **kwargs):
    device_entries = []
    user_mailingdict = {}
    messages = ()

    if(action == "post_add"):
        for device_id in pk_set:
            for entry in DeviceEntry.objects.filter(device=device_id):
                user_email = str(entry.unique_room.user)
                room_name = entry.unique_room.room_name
                if ( user_email not in user_mailingdict):
                    # e.g a[user@aol.de]
                    user_mailingdict[user_email] = {}
                
                if not (user_mailingdict[user_email].__contains__(room_name)):
                    user_mailingdict[user_email][room_name] = [] 
                user_mailingdict[user_email][room_name].append(entry)
        for user in user_mailingdict.keys():
            context = {
                    'username': user,
                    "rooms" : user_mailingdict[user], 
                    "vulnerability": instance.description, 
                    }
            if (list(CustomUser.objects.filter(email=user).values_list("country"))[0][0] == 'DE'):
                subject = "Neue Sicherheitslücke die dich betrifft"
                email_text = render_to_string("smarthome/email_body_german.html",context)
            else:
                subject = "A new Vulnerability added which concerns you "
                email_text = render_to_string("smarthome/email_body_english.html",context)
            messages = messages + ((subject, email_text, "davidschmidt777@t-online.de", [user_email]),)

        print(len(messages))
        send_mass_mail((messages))
            
        pass
            


class PrivacyIssue(models.Model):
    device_id = models.ManyToManyField(Device,verbose_name= _("Privacy Issue affects the following devices:"))
    discovery = models.DateField(max_length=20)
    description = models.CharField(max_length=300)
    paper_url = models.URLField(max_length=500,verbose_name= _("URL to the Article to the Privacy Issue"))
    patch_date = models.DateField(verbose_name= _("Privacy Issue got resolved/updated on:"),null=True,blank=True)
    url_patch = models.URLField(max_length=500,verbose_name= _("URL to the Privacy Issue update"),blank=True)


class DeviceEntry(models.Model):
    id = models.AutoField(primary_key=True)
    unique_room = models.ForeignKey("Room",on_delete=models.CASCADE)
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    connector = models.ForeignKey(Connector,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["unique_room","device","connector","quantity"],name="unique_entry")]
        verbose_name = _("Device Entry")
        verbose_name_plural = _("Device Entries")


    def __str__(self):
        return self.device.manufacturer +" "+ self.device.name +" "+ str(self.quantity) 


#
# device_list list of dict with {device_id,connector}
#

    @staticmethod
    def setEntries(a_room,device_list_dict):
        # get list of device_ids
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
        return self.room_name +"   " +str(self.user) 


    @staticmethod
    def GetExistingRoomNames(a_email):
        room_names = []
        for room in Room.objects.filter(user=a_email):
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


"""
class App(models.Model):
    name = models.CharField(primary_key=True,max_length=60)
    supported_device = models.ManyToManyField(Device,verbose_name=("The App works with the following Devices:"))
    developer = models.CharField(max_length=200)


class AppUpdate(models.Model):
    app_name = models.ManyToManyField(App,verbose_name= _("Update belongs to"))
    version_number = models.CharField(primary_key=True,max_length=50)
    releasedate = models.DateField(blank=True) 
    changelog = models.CharField(max_length=200)
    
"""









