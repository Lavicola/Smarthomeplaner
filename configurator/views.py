from django.http import JsonResponse
from django.http import HttpResponse

from django.shortcuts import render
from smarthome.models import Device,Firmware,Room,DeviceEntry
from django.template import loader
from .forms import SmarthomeMapForm
from configurator.models import CanvasMap
import json

# Create your views here.





def congifuration(request):
    l_email = request.user.email
    l_rooms = Room.objects.filter(user=l_email).values()
    l_fullrooms = {}
    for room in l_rooms:
        l_fullrooms[room["room_name"]] = []
        devices = DeviceEntry.objects.filter(unique_room=room["id"])
        for device in devices:
            l_fullrooms[room["room_name"]].append(device)

    print(l_fullrooms["WC"])

    context =  {'rooms': l_fullrooms}
    


    template = loader.get_template('configurator/room_configurations.html')

    return HttpResponse(template.render(context, request))








def index(request):
    devices = Device.objects.all()
    categories = Device.Device_Category.choices
    context = {
        'devices': devices,
        "categories":categories,
    }
    
    template = loader.get_template('configurator/smarthome_configurator.html')
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
    if request.method == 'POST':
        email = request.user.email
        json_data = json.loads(request.body)
        room_names = list(json_data.keys())


        Room.DeleteUnusedRooms(email,list(json_data.keys()))   
        Room.CreateRooms(email,list(json_data.keys()))
        for room_name in room_names:            
            DeviceEntry.setEntries(email,room_name,json_data[room_name])        

    return HttpResponse('/thanksssss/')



