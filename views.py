from benchmarks.posts.models import Post
from django.shortcuts import render_to_response
from django.template import RequestContext

def homepage(request):
	featured_posts = Post.objects.filter(sticky=True)
	latest_posts = Post.objects.filter(sticky=False).order_by('published')[:5]
	return render_to_response('homepage.html', 
		{'featured_posts': featured_posts,
		 'latest_posts': latest_posts}, context_instance = RequestContext(request))
