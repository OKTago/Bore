# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse

from helpers import get_cookie_name, redirect_to_auth, get_token

from facebook import GraphAPI


def index(request):
   # print request.COOKIES['sessionid'];
    code = request.GET.get('code', None)
  #  return HttpResponse("")
    if code is None:
        return HttpResponse(redirect_to_auth())
    else:
        token = get_token(code)
        face = GraphAPI(token)
        profile = face.get_object("me")
        print profile
        return HttpResponse(token)
        # TODO: get token and store into db
        #return render_to_response('face/base_index.html', {}, 
        #                       context_instance=RequestContext(request))

