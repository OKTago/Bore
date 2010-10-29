from meta.models import MetaType, Reload
from meta.lib.manager import MetaMan

class MetaObjectsMiddleware(object):
    def process_request(self, request):
        if Reload.required():
            Reload.unschedule()
            metaMan = MetaMan()
            metaMan.buildClasses(MetaType)
            # NOTE: works with apache and wsgi in daemon mode only
            #       http://code.google.com/p/modwsgi/wiki/ReloadingSourceCode
            
            # TODO: find a workaround for django development server
            import signal, os
            os.kill(os.getpid(), signal.SIGINT)
        return

