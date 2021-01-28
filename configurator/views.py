from django.http import JsonResponse
from django.http import HttpResponse

from django.shortcuts import render
from smarthome.models import Device,Firmware
from django.template import loader
from .forms import SmarthomeMapForm
from configurator.models import CanvasMap
import json

# Create your views here.



def index(request):
    devices = Device.objects.all()
    categories = Device.Device_Category.choices
    context = {
        'devices': devices,
        "categories":categories,
    }
    
    template = loader.get_template('configurator/index.html')
    return HttpResponse(template.render(context, request))


def getCanvas(request):
    canvas_map = CanvasMap.objects.get(email=request.user.email)
    canvas_json = json.dumps(canvas_map.canvas_map)
    return JsonResponse(canvas_json, safe=False)


def setCanvas(request):
    if request.method == 'POST':
        form = SmarthomeMapForm(request.POST)
        if form.is_valid():
            map = CanvasMap(request.user.email,form.cleaned_data["canvas_map"])
            CanvasMap.save(map)
        else:
            return HttpResponse('/error/') #
        return HttpResponse('/thanks/') # Redirect after POST
    return HttpResponse('/error/') #


def saveRooms(request):
    json_data = json.loads(request.body) 
    print(json_data)


    return HttpResponse('/thanksssss/')



