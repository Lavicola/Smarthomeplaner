from django.contrib import admin
from.models import *



# Register your models here.
admin.site.register(Device)
admin.site.register(Firmware)
admin.site.register(Vulnerability)
admin.site.register(Connector)
admin.site.register(PrivacyInformation)
admin.site.register(Room)
admin.site.register(DeviceEntry)
admin.site.register(Standard)

