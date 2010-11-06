from django.conf.urls.defaults import *
from meta.manager import metaman

urlpatterns = patterns('meta',
    (r'^$', 'views.index'),
    (r'^man/', include(metaman.urls)),
)
