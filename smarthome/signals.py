from django.db.models.signals import post_save
from smarthome.models import Vulnerability
from django.dispatch import receiver
from django.db.models import signals
from django.db.models.signals import m2m_changed

#send emal to users if a new Vulnerability was added
@receiver(m2m_changed, sender=Vulnerability.device_id.through)
def notify_users_email(sender,instance,**kwargs):   
    print("called")
    message = ""
    devices = instance.device_id.all()
    discovery_date = instance.discovered_date
    description = instance.description
    link = instance.url
    message= str(discovery_date) + description + link
    print(message)
    results = Vulnerability.objects.all()
    print(devices)












    