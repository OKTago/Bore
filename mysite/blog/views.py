# Create your views here.
from blog.models import Post

from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    posts = Post.objects.all().order_by("-pub_date")
    return render_to_response('blog/base_index.html', {'posts': posts}, 
                               context_instance=RequestContext(request))

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render_to_response('blog/base_post.html', {'post': post}, 
                               context_instance=RequestContext(request))
