from django.http import JsonResponse
from django.http import HttpResponse

from django.shortcuts import render
from smarthome.models import Device,Room,DeviceEntry,Category,Vulnerability,Connector
from django.template import loader
from .forms import AJAXForm
from configurator.models import CanvasMap
import json


def configuration(request):
    l_tabledata = {}
    table_color = ""
    if request.user.is_authenticated:
        l_email = request.user.email
        l_rooms = Room.objects.filter(user=l_email).values()
        for room in l_rooms:
            l_tabledata[room["name"]] = []
            device_entries = DeviceEntry.objects.filter(room=room["id"])
            for device_entry in device_entries:
                if(Vulnerability.objects.filter(device_id=device_entry.device_id,patch_date__isnull=True).count() != 0): 
                    table_color = "red-column"
                else:
                    table_color = "white-column"                
                l_tabledata[room["name"]].append((device_entry,table_color))
                
    context =  {
        'table_informations': l_tabledata
        }
    template = loader.get_template('configurator/room_configurations.html')

    return HttpResponse(template.render(context, request))


def index(request):
    devices = Device.objects.all()
    categories = Category.objects.all()
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



def saveConfiguration(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            email = request.user.email            
            post_data = json.loads(request.body.decode('utf-8'))
            form = AJAXForm(post_data)                        
            if form.is_valid():                                
                json_data = form.cleaned_data["json_data"]
                canvas_map = form.cleaned_data["canvas_map"]
                #Step 1 Save Room Configuration
                room_names = list(json_data.keys())
                Room.DeleteUnusedRooms(email,list(json_data.keys()))   
                Room.CreateRooms(email,list(json_data.keys()))
                for room_name in room_names:
                    room = Room.GetRoom(a_email=email,a_name=room_name)
                    DeviceEntry.setEntries(room,json_data[room_name])        
                    DeviceEntry.DeleteUnusedEntries(room,json_data[room_name])
                #Step 2 Save Canvas Map
                CanvasMap.save(CanvasMap(request.user.email,canvas_map))
                return HttpResponse('Success', status=200)
        return HttpResponse('Unauthorized', status=401)
    return HttpResponse()



