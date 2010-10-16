import os
import sys
import site

PWD = os.path.dirname(__file__)
site.addsitedir(PWD+"/lib")
sys.path.append(PWD)

os.environ['DJANGO_SETTINGS_MODULE'] = 'apps.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
