from django.db.models.signals import post_save
from smarthome.models import Vulnerability
from django.dispatch import receiver
from django.db.models import signals


@receiver(post_save, sender=Vulnerability)
def notify_users_email(sender,instance,created,**kwargs):   
    message = ""
    discovery_date = instance.discovered_date
    description = instance.description
    link = instance.url
    message= str(discovery_date) + description + link
    print(message)










    