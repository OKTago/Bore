from django.conf.urls.defaults import *

urlpatterns = patterns('meta',
    (r'^$', 'views.index'),
#    (r'^meta/', include(meta.site.urls)),
)
