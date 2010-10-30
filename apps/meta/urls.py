from django.conf.urls.defaults import *

urlpatterns = patterns('meta',
    (r'^$', 'views.index'),
    (r'syncmeta$', 'views.syncmeta'),
)
