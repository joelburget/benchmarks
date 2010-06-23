from benchmarks.posts.models import Post
from django.shortcuts import render_to_response

def homepage(request):
	featured_posts = Post.objects.filter(sticky=True)
	latest_posts = Post.objects.all()[:5]
	return render_to_response('homepage.html', 
		{'featured_posts': featured_posts,
		 'latest_posts': latest_posts})