from django.conf.urls.defaults import *

urlpatterns = patterns('face.views',
    (r'^$', 'index'),
    (r'^delete/(\d+)/$', 'remove_exfriend')
)
