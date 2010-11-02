from django.conf.urls.defaults import *

urlpatterns = patterns('meta',
    (r'^$', 'views.index'),
    (r'^mt/(?P<type_name>.*)/$', 'views.meta'),
)
