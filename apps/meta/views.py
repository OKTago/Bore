# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

from meta.models import MetaType 
from meta.lib.manager import MetaMan

def index(request):
    # non dovrebbe essere qui
    # sync_meta_models andrebbe chiamato solo alla definizione di un nuovo
    # tipo
    metaMan = MetaMan()
    metaTypes = MetaType.objects.all()
    metaMan.buildClasses(metaTypes)


    #t1 = metaMan.getClass('Type1')
    data = {}
    data['name'] = "MetaTypes"
    #data['objects'] = t1.objects.all()
    data['objects'] = MetaType.objects.all()
    return render_to_response('meta/base_index.html', data,
                               context_instance=RequestContext(request))

