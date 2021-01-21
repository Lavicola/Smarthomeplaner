from django.contrib import admin
from configurator.models import Device
from configurator.models import Firmware
from configurator.models import Vulnerability


# Register your models here.
admin.site.register(Device)
admin.site.register(Firmware)
admin.site.register(Vulnerability)