from meta.models import MetaType 
from meta.lib.manager import MetaMan

class MetaObjectsMiddleware(object):
    def process_request(self, request):
        print "test request"
        return

    def process_response(self, request, response):
        metaMan = MetaMan()
        metaTypes = MetaType.objects.all()
        metaMan.buildClasses(metaTypes)
        print "test response"
        return response

