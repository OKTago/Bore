from django.conf.urls.defaults import *

urlpatterns = patterns('blog.views',
    (r'^$', 'index'),
    (r'^post/(?P<post_id>\d+)/$', 'post'),
)
