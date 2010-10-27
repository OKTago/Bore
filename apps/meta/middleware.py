from meta.models import MetaType 
from meta.lib.manager import MetaMan

class MetaObjectsMiddleware(object):
    def process_request(self, request):
        metaMan = MetaMan()
        metaTypes = MetaType.objects.all()
        metaMan.buildClasses(metaTypes)
       # print "test request"
        return

    def process_response(self, request, response):
        #print "test response"
        return response

