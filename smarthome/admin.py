from django.contrib import admin
from.models import *



# Register your models here.
admin.site.register(Device)
admin.site.register(Firmware)
admin.site.register(Vulnerability)
admin.site.register(Connector)
admin.site.register(PrivacyIssue)
admin.site.register(Category)
admin.site.register(Room)
admin.site.register(DeviceEntry)

