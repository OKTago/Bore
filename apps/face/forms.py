from django.forms import ModelForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, get_object_or_404
from face.models import Friend

class FriendForm(ModelForm):
    class Meta:
        model = Friend

@csrf_protect
def friend(request, id):
    if id:
        friend = Friend.objects.get(pk=id)
        if request.method == "POST":
            form = FriendForm(request.POST, instance=friend)
            if form.is_valid():
                form.save()
        else:
            form = FriendForm(instance=friend)
    else:
        if request.method == "POST":
            form = FriendForm(request.POST)
            if form.is_valid():
                form.save()
        else: 
            form = FriendForm()
    data = {}
    data['form'] = form
    return render_to_response('face/base_form.html', data,
                        context_instance = RequestContext(request))
