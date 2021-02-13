from django.shortcuts import render
from api.serializers import CanvasMap
from django.http import HttpResponse
from .models import Device
from django.http import Http404



# Create your views here.


def index(request):

    return HttpResponse("You reached me!")


def detail(request,device_id):
    try:
        device = Device.objects.get(pk=device_id)
    except Device.DoesNotExist:
        raise Http404("Device does not exist")
    return HttpResponse("You're looking at device %s." % device_id)
    return render(request, 'device/detail.html', {'device': device})



def devices_overview(request):
    devices = Device.objects.all()
    
    template = loader.get_template('configurator/devices.html')
    context = {
        'devices': devices,
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
    






