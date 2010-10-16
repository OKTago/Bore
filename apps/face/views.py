# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist 
from django.views.decorators.http import require_POST

from helpers import get_cookie_name, redirect_to_auth, get_token

from facebook import GraphAPI
from face.models import UserSession
from face.models import Friend

def index(request):
    code = request.GET.get('code', None)
    # check if we have a token into session
    token = request.session.get('token', None)
    got_token =True 
    if token is None:
        if code is None:
            # we don't have the code and the token
            # so we must redirect
            return HttpResponse(redirect_to_auth())
        else:
            # we have the code. Request a token
            token = get_token(code)
            got_token = True
    face = GraphAPI(token)
    profile = face.get_object("me")
    first_name = profile['first_name']
    last_name = profile['last_name']
    uid = profile['id']
    if got_token:
        try:
            # update token if object exists
            us = UserSession.objects.get(uid=uid)
            us.token = token
            us.save()
        except ObjectDoesNotExist:
            us = UserSession(
                    uid=uid, 
                    token=token, 
                    first_name=first_name, 
                    last_name=last_name, 
                    enabled=False)
            us.save()
        request.session['token'] = token
    data = {}
    data['profile'] = profile
    data['deleted_friend'] = []
    deleted_friend = Friend.objects.filter(user_id=uid, deleted=True) 
    for friend in deleted_friend:
        friend_id = friend.friend_id
        friend_profile = face.get_object(friend_id)
        data['deleted_friend'].append(friend_profile)
    return render_to_response('face/base_index.html', data, 
                           context_instance=RequestContext(request))

@require_POST
def remove_exfriend(request, friend_id):
    token = request.session.get('token', None)
    if token is None:
        return HttpResponseRedirect("/")
    
    f = Friend.objects.get(friend_id=friend_id)
    f.delete()
    return HttpResponse(friend_id)
