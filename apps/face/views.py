# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist 

from helpers import get_cookie_name, redirect_to_auth, get_token

from facebook import GraphAPI
from face.models import UserSession
from face.models import Friends 


def index(request):
    code = request.GET.get('code', None)
    token = request.session.get('token', None)
    if token is None:
        if code is None:
            return HttpResponse(redirect_to_auth())
        else:
            token = get_token(code)

    face = GraphAPI(token)
    profile = face.get_object("me")
    first_name = profile['first_name']
    last_name = profile['last_name']
    uid = profile['id']
    #us = UserSession(uid=uid, token=token, first_name=first_name, last_name=last_name, enabled=False)
    #us.save()
    try:
        UserSession.objects.filter(uid=uid).update(token=token, first_name=first_name, last_name=last_name, enabled=False)
    except ObjectDoesNotExist:
        us = UserSession(uid=uid, token=token, first_name=first_name, last_name=last_name, enabled=False)
        us.save()
    request.session['token'] = token
    return HttpResponse(first_name)
    # TODO: get token and store into db
    #return render_to_response('face/base_index.html', {}, 
    #                       context_instance=RequestContext(request))


