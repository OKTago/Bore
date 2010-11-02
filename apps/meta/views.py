# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from meta.models import MetaType, Reload

def index(request):
    data = {}
    data['name'] = "MetaTypes"
    data['objects'] = MetaType.objects.all()
    return render_to_response('meta/base_index.html', data,
                               context_instance=RequestContext(request))

def meta(request, type_name):
    return HttpResponse("meta: %s" % type_name)
