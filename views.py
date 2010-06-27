from benchmarks.posts.models import Post
from django.shortcuts import render_to_response
from django.template import RequestContext
from benchmarks.extended_comments.models import ExtendedComment

def homepage(request):
  #featured posts always stay on the homepage
  featured_posts = Post.objects.filter(sticky=True)
  latest_posts = Post.objects.filter(sticky=False).order_by('-published')[:5]
  latest_discussion = ExtendedComment.objects.all().order_by('-submit_date')[:5]
  return render_to_response('homepage.html', {
                                              'featured_posts': featured_posts,
                                              'latest_posts': latest_posts, 
                                              'latest_discussion' : latest_discussion, 
                                            }, context_instance = RequestContext(request))
