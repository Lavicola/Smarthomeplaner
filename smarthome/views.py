from django.shortcuts import render
from api.serializers import CanvasMap
from django.http import HttpResponse


# Create your views here.


def index(request):

    return HttpResponse("You reached me!")


def device_detail(request,device_id):
    

    return HttpResponse("You're looking at device %s." % device_id)


def devices_overview(request):


    devices = Device.objects.all()
    cate = Device.Device_Category.choices
    
    template = loader.get_template('configurator/devices.html')
    context = {
        'devices': devices,
        "cat":cate,
    }
    return HttpResponse(template.render(context, request))

    
def firmware_list(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices,many=True)
    return JsonResponse(serializer.data, safe=False)



def save_rooms(request):
    for room in json_data:
        for devices in json_data[room]:
            print(devices)
    






