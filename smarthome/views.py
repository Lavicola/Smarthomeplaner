from django.shortcuts import render
from api.serializers import CanvasMap
from django.http import HttpResponse
from .models import Device
from django.http import Http404
from django.template import loader
from .models import Vulnerability,Device


# Create your views here.



def device_overview(request,device_name):
    try:
        
        device = Device.objects.get(name=device_name)
        print(device.name)
    except Device.DoesNotExist:
        raise Http404("Device does not exist")
    context = {
        "device" : device,
    }
    template = loader.get_template('smarthome/device_overview.html')
    return HttpResponse(template.render(context, request))





def devices_overview(request):
    devices = Device.objects.all()
    
    template = loader.get_template('smarthome/devices.html')
    context = {
        'devices': devices,
    }
    return HttpResponse(template.render(context, request))





