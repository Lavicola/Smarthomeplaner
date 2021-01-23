from django.db import models
from django.utils.translation import gettext_lazy as _ #translation
from users.models import AbstractBaseUser
from django.contrib.auth import settings



# Create your models here.

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to='Device')
    releasedate = models.DateField()
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


    def __str__(self):
        return self.name +" " + self.manufacturer_name + "  V" + self.generation



class Interface(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    connector = models.CharField(max_length=30)


class Firmware(models.Model):
    firmware_id = models.AutoField(primary_key=True)
    Compatibility_list = models.ManyToManyField(Device,verbose_name= _("Firmware Kompatibel mit"))
    version_number = models.CharField(max_length=50,verbose_name= _("Versionsnummer"))
    changelog = models.CharField(verbose_name=_("Änderungen"), max_length=500)
    releasedate = models.DateField(verbose_name=_("Erscheinungsdatum"))

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


class CanvasMap(models.Model):
    email = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key=True)
    canvas_map = models.JSONField()
    

    






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










