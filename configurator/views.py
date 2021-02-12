from django.http import JsonResponse
from django.http import HttpResponse

from django.shortcuts import render
from smarthome.models import Device,Firmware,Room,DeviceEntry
from django.template import loader
from .forms import SmarthomeMapForm,AJAXSaveRoomForm
from configurator.models import CanvasMap
import json

# Create your views here.





def congifuration(request):
    l_fullrooms = {}
    if request.user.is_authenticated:
        l_email = request.user.email
        l_rooms = Room.objects.filter(user=l_email).values()
        for room in l_rooms:
            l_fullrooms[room["room_name"]] = []
            devices = DeviceEntry.objects.filter(unique_room=room["id"])
            for device in devices:
                l_fullrooms[room["room_name"]].append(device)
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
    if request.method == 'POST':
        if request.user.is_authenticated:
            canvas_map = CanvasMap.objects.get(email=request.user.email)
            canvas_json = json.dumps(canvas_map.canvas_map)
            return JsonResponse(canvas_json, safe=False)
        else:
            return HttpResponse('Unauthorized', status=401)
    return HttpResponse() #



def setCanvas(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = SmarthomeMapForm(request.POST)
            if form.is_valid():
                map = CanvasMap(request.user.email,form.cleaned_data["canvas_map"])
                CanvasMap.save(map)
                return HttpResponse('/thanks/') 
        else:
                return HttpResponse('Unauthorized', status=401)
    return HttpResponse() 


def saveRooms(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            email = request.user.email
            form = AJAXSaveRoomForm(request.POST)
            if form.is_valid():
                json_data = form.cleaned_data["json_data"]
                room_names = list(json_data.keys())
                Room.DeleteUnusedRooms(email,list(json_data.keys()))   
                Room.CreateRooms(email,list(json_data.keys()))
                for room_name in room_names:
                    room = Room.GetRoom(a_email=email,a_room_name=room_name)
                    DeviceEntry.setEntries(room,json_data[room_name])        
                    DeviceEntry.DeleteUnusedEntries(room,json_data[room_name])
                return HttpResponse('/thanksssss/')
        return HttpResponse('Unauthorized', status=401)
    return HttpResponse()



