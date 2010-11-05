from django.http import HttpResponse

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
        print self.model
        return HttpResponse("index")

    def single(self, request, objId):
        """
        Render a single object
        """
        return HttpResponse("single")

    def add(self, request):
        return HttpResponse("add")

    def delete(self, request, objId):
        return HttpResponse("delete")

    def change(self, request, objId):
        return HttpResponse("change")

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url, include
        urlpatterns = patterns('',
            url(r'^$', self.index),
            url(r'^add/$', self.add),
            url(r'^(.+)/delete/$', self.delete),
            url(r'^(.+)/change/$', self.change),
            url(r'^(.+)/$', self.single),
        )
        return urlpatterns
    urls = property(get_urls)
