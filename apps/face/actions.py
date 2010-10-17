from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from face.models import Friend

@require_POST
def remove_exfriend(request, id):
    token = request.session.get('token', None)
    if token is None:
        return HttpResponseRedirect("/")
    
    f = Friend.objects.get(pk=id)
    f.delete()
    return HttpResponse(id)
