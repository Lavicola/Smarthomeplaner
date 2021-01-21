from django.http import HttpResponse
from django.template import loader

from configurator.models import Device
from configurator.models import Firmware
from configurator.models import Vulnerability
#REST
from rest_framework import viewsets
from .serializers import FirmwareSerializer,DeviceSerializer




def index(request):
    latest_question_list = Device.objects.order_by('releasedate')[:5]
    template = loader.get_template('configurator/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def device_detail(request,device_id):


    return HttpResponse("You're looking at device %s." % device_id)


def devices_overview(request):

    
    devices = Device.objects.all()
    template = loader.get_template('configurator/devices.html')
    context = {
        'devices': devices,
    }
    return HttpResponse(template.render(context, request))

#REST
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
from django.http import JsonResponse


def firmware_list(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices,many=True)
    return JsonResponse(serializer.data, safe=False)


#REST

import random
import json
from .viewsets import DeviceViewSet

def acdc(request):

    view = DeviceViewSet()


    out = view.list()
    #template = loader.get_template('configurator/vue_list.html')
    return HttpResponse(out)

    return HttpResponse(template.render(context, request))

















