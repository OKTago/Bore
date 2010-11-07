from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.forms.models import modelform_factory
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import list_detail

def get_model_fields(model):
    opts = model._meta
    ret = []
    for f in opts.fields + opts.many_to_many:
        if f.formfield():
            ret.append(f.name)

    return ret

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
        obj_info = {
            "queryset": self.model.objects.all(),
            "template_name": "meta/list.html",
            "template_object_name" : "obj",
            "extra_context" : {"view" : reverse(self.__url_name('index'))}
        }
        return list_detail.object_list(request, **obj_info)

    def details(self, request, objId):
        """
        Render a single object
        """
        obj = self.model.objects.get(pk=objId)
        from django.forms.models import fields_for_model
        fields_names = get_model_fields(self.model)
        fields = {}
        context = {}
        for f in fields_names:
            value = getattr(obj, f)
            fields[f] = value
            # export fields directly to context for custom views
            context[f] = value
        context['fields'] = fields
        return render_to_response([
                            'meta/%s_details.html' % self.model.__name__.lower(),
                            'meta/details.html'], 
                            context, context_instance=RequestContext(request))

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
