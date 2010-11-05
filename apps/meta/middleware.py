from meta.models import Reload
from meta.manager import MetaMan

class MetaObjectsMiddleware(object):
    def process_request(self, request):
        if Reload.required():
            Reload.unschedule()
            metaMan = MetaMan()
            metaMan.build_classes()
            # NOTE: works with apache and wsgi in daemon mode only
            #       http://code.google.com/p/modwsgi/wiki/ReloadingSourceCode
            
            # TODO: find a workaround to reload django development server
            server = request.META.get('wsgi.file_wrapper', None)
            if server is not None and server.__module__ == 'django.core.servers.basehttp':
                print "\n"
                print "You must restart the development server for changes to take effect"
                print "\n"
            else :
                # Commented here. This approach will restart only current process
                # becouse other daemons will have Reload.required() = False
                # Touching the WSGI_FILE should restart all daemons instead. (At least I
                # hope :) Need testing)
                #import signal, os
                #os.kill(os.getpid(), signal.SIGINT)
                import os
                from settings import WSGI_FILE
                # simulating touch (should restart all daemons processes)
                os.utime(WSGI_FILE, None)
        
        return

