# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    #t1 = metaMan.getClass('Type1')
    data = {}
    data['name'] = "MetaTypes"
    #data['objects'] = t1.objects.all()
    data['objects'] = MetaType.objects.all()
    return render_to_response('meta/base_index.html', data,
                               context_instance=RequestContext(request))

