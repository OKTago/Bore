from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.forms.models import modelform_factory
from django.core.urlresolvers import reverse

"""
Action class for meta model.
"""
class Actions:
    def __init__(self, model):
        self.model = model
    
    def index(self, request):
        """
        Show all model objects
        """
        return HttpResponse("index: %s" % self.model._meta)

    def details(self, request, objId):
        """
        Render a single object
        """
        obj = self.model.objects.get(pk=objId)
        return HttpResponse("details")

    def add(self, request):
        ModelForm = modelform_factory(self.model)
        if request.method == 'POST':
            form = ModelForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse(self.__url_name("index")))
        else:
            form = ModelForm()
        context = {
            'form': form
        }
        return render_to_response('meta/add.html', context, 
                            context_instance=RequestContext(request))

    def delete(self, request, objId):
        return HttpResponse("delete")

    def change(self, request, objId):
        return HttpResponse("change")

    def __url_name(self, view_name):
        return '%s_%s' % (self.model.__name__, view_name)

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urlpatterns = patterns('',
            url(r'^$', self.index, name = self.__url_name("index")),
            url(r'^add/$', self.add, name = self.__url_name("add")),
            url(r'^(.+)/delete/$', self.delete, name = self.__url_name("delete")),
            url(r'^(.+)/change/$', self.change, name = self.__url_name("change")),
            url(r'^(.+)/$', self.details, name = self.__url_name("details")),
        )
        return urlpatterns
    urls = property(get_urls)
