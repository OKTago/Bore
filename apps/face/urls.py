from django.conf.urls.defaults import *

urlpatterns = patterns('face.views',
    (r'^$', 'index'),
    (r'^exfriend/(^P<friend_id>\d+)/delete$', 'remove_exfriend')
)
