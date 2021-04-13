from django.db import models
from django.utils.translation import gettext_lazy as _ #translation
from users.models import AbstractBaseUser
from django.contrib.auth import settings
from users.models import CustomUser
from django.utils import timezone
from django.db.models.signals import m2m_changed, post_delete, pre_save
from django.dispatch import receiver
from django.template.loader import get_template,render_to_string
from django.template import Context
from django.core.mail import send_mass_mail



# Create your models here.


class Connector(models.Model):
    connector = models.CharField(max_length=30)

    def __str__(self):
        return self.connector

    class Meta:
        verbose_name = _("Connector")
        verbose_name_plural = _("Connectors")
        constraints = [models.UniqueConstraint(fields=["connector"],name="unique_connector")]

    # get the connector id e.g E14 --> ID=1
    @staticmethod
    def GetConnectorID(a_connector_name):
        return Connector.objects.filter(connector=a_connector_name).values_list("id",flat=True)[0]
    
    #get the connector object over name
    @staticmethod
    def GetConnector(a_connector_name):
        return Connector.objects.filter(connector=a_connector_name).get()
        


class Standard(models.Model):
    standard = models.CharField(max_length=30,primary_key=True)
    def __str__(self):
        return self.standard

    class Meta:
        verbose_name = _("Standard")
        verbose_name_plural = _("Standard")


    #get the Standard object
    @staticmethod
    def GetStandard(a_standard):
        return Standard.objects.filter(standard=a_standard).get()



class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to='Device')
    connector = models.ManyToManyField(Connector)
    standard = models.ManyToManyField(Standard,blank=True)
    manufacturer = models.CharField(max_length=200) 
    generation = models.CharField(max_length=10)
    compatible_device = models.ManyToManyField('self',verbose_name=_("Compatible with"),blank=True)
    
    class Device_Category(models.TextChoices):
        SMART_LIGHTNING = "Smart_Lightning", _("Smart_Lightning")
        SMART_LOCK = "Smart_Lock" , _("Smart_Lock")
        VIRTUAL_ASSISTANT = "Virtual_Assistant", _("Virtual_Assistant")

    category = models.CharField(
        max_length=20,
        choices=Device_Category.choices
    )

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        constraints = [models.UniqueConstraint(fields=["name","manufacturer","generation"],name="unique_device")]

    def __str__(self):
        return self.name +" " + self.manufacturer + "  V" + self.generation 


    @staticmethod
    def GetDevice(device_id):
        return Device.objects.filter(id=device_id).first()

    @staticmethod
    def GetCategories():
        choices_tuple = Device.Device_Category.choices
        choices = []
        for category in choices_tuple:
            choices.append(category[0])    
        return choices







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



# this signals sends the name 
@receiver(m2m_changed, sender=Vulnerability.device_id.through)
def notify_users(sender,action,pk_set,instance, **kwargs):
    email_sender = "smarthomeplaner@gmail.com"
    #check if a new vulnerability was added
    if(action == "post_add"):
        #maybe a closed vulnerability was added if so we dont want to send an email
        if(instance.patch_date is not None):
            device_entries = []
            user_mailingdict = {}
            messages = ()
            #pk_set is a list of ids which are vulnerable
            for device_id in pk_set:
                for entry in DeviceEntry.objects.filter(device=device_id):
                    user_email = str(entry.room.user)
                    name = entry.room.name
                    if ( user_email not in user_mailingdict):
                        # e.g user_mailingdict[user@aol.de]
                        user_mailingdict[user_email] = {}           
                        # add the roomname to the nested hashmap if necessary         
                    if not (user_mailingdict[user_email].__contains__(name)):
                        user_mailingdict[user_email][name] = [] 
                    user_mailingdict[user_email][name].append(entry)
            for user in user_mailingdict.keys():
                # the context holds every room with every device which is vulnerable
                context = {
                        'username': user,
                        "rooms" : user_mailingdict[user], 
                        "vulnerability": instance.description, 
                        }
                if (list(CustomUser.objects.filter(email=user).values_list("language_choice"))[0] == 'de-de'):
                    subject = "Neue Sicherheitslücke die dich betrifft"
                    email_text = render_to_string("smarthome/email_body_german.html",context)
                else:
                    subject = "A new Vulnerability added which concerns you "
                    email_text = render_to_string("smarthome/email_body_english.html",context)
                    #In order to send mass emails we create a tuple of messages which consists of
                #every subject is in the language of the user and now we can send every email to the users
                messages = messages + ((subject, email_text, email_sender, [user_email]),)
            send_mass_mail((messages))
        pass
            


class DataProtectionInformation(models.Model):
    device_id = models.ManyToManyField(Device,verbose_name= _("Privacy Concern affects the following devices:"))
    description = models.CharField(max_length=300)
    paper_url = models.URLField(max_length=500,verbose_name= _("URL to the Article to the Privacy Concern"))

    class Meta:
        verbose_name = _("Data Protection Information")
        verbose_name_plural = _("Data Protection Information")


    def __str__(self):
        return self.description 




class DeviceEntry(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey("Room",on_delete=models.CASCADE)
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    connector = models.ForeignKey(Connector,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["room","device","connector","quantity"],name="unique_entry")]
        verbose_name = _("Device Entry")
        verbose_name_plural = _("Device Entries")


    def __str__(self):
        return self.device.manufacturer +" "+ self.device.name +" "+ str(self.quantity) 


# device_list list of dict with {device_id,connector}
    @staticmethod
    def setEntries(a_room,device_list_dict):
        # get list of device_ids
        device_list = [a_dict["device_id"] for a_dict in device_list_dict]
        # get the unique connectors
        unique_dict_list = list(map(dict, set(tuple(sorted(sub.items())) for sub in device_list_dict))) 
        unique_connector_list = [a_dict["connector"] for a_dict in unique_dict_list]
        # loop variables
        l_connector = None
        for id in set(device_list):
            device_object = Device.GetDevice(id)
            for connector in unique_connector_list:
                l_connector = Connector.GetConnector(connector)
                quantity = DeviceEntry.GetDeviceQuantity(device_list_dict,id,connector)
                if(quantity == 0):
                    continue
                else:
                    if(DeviceEntry.exists(a_room,device_object,l_connector)):
                        DeviceEntry.UpdateQuantity(a_room,device_object,l_connector,quantity)
                    else:
                        DeviceEntry.setEntry(a_room,device_object,l_connector,quantity)
        return 


    @staticmethod
    def DeleteUnusedEntries(a_room,device_list_dict):
        device_entries = DeviceEntry.objects.filter(room=a_room)
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
        DeviceEntry.save(DeviceEntry(room=room,device=device,connector=a_connector,quantity=a_quantity))
        return True

    @staticmethod
    def UpdateQuantity(a_room,a_device,a_connector,a_quantity):
        DeviceEntry.objects.filter(room=a_room,device=a_device,connector=a_connector).update(quantity=a_quantity)
        return True

    @staticmethod
    def DeleteEntry(a_room,a_device,a_connector):
        DeviceEntry.objects.get(room=a_room,connector=a_connector,device=a_device).delete()
        return 

    # gives the current Device Entry quantity which is saved in the database back. 
    @staticmethod
    def GetCurrentDeviceQuantity(a_room,a_device):
        return DeviceEntry.objects.only("quantity").get(room=a_room,device=a_device).quantity


#a_room = roob object 
# device = device object
# connector = connector
    @staticmethod
    def exists(a_room,a_device,a_connector):
        if( DeviceEntry.objects.filter(room=a_room,device=a_device,connector=a_connector).count() == 0 ):
            return False
        return True




class Room(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user","name"],name="room")]

    def __str__(self):
        return self.name +"   " +str(self.user) 


    @staticmethod
    def GetExistingRoomNames(a_email):
        names = []
        for room in Room.objects.filter(user=a_email):
            names.append(room.name)
        return names


    @staticmethod
    def DeleteUnusedRooms(a_email,a_names):
        current_names = Room.GetExistingRoomNames(a_email)
        for name in current_names:
            if name not in a_names:
                Room.delete(a_email,name)
        return 


    @staticmethod
    def GetRoom(a_email,a_name):
                
        return Room.objects.filter(user=a_email,name=a_name).first()


    @staticmethod
    def exists(a_email,a_name):

        return Room.objects.filter(user=a_email,name=a_name).exists()


    @staticmethod
    def create(a_email,a_name):
        Room.save(Room(user_id=a_email,name=a_name))
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
        Room.objects.filter(user_id=a_email,name=a_names).delete()
        return True









