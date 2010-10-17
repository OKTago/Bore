from django.conf.urls.defaults import *

urlpatterns = patterns('face',
    (r'^$', 'views.index'),
    (r'^friend/(\d*)$','forms.friend'),
    (r'^delete/(\d+)/$', 'actions.remove_exfriend')
)
