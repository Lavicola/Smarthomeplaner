from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import FundamentalsEntry


# Create your views here.



def index(request):
    entries = FundamentalsEntry.objects.all()
    
    template = loader.get_template('basics/basics.html')

    context = {
        'entries': entries,
    }
    return HttpResponse(template.render(context, request))
