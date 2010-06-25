from benchmarks.posts.models import Post
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.comments.models import Comment
from django.contrib.comments.views.comments import post_comment
from django.http import HttpRequest
import html5lib
from html5lib import sanitizer

def homepage(request):
  featured_posts = Post.objects.filter(sticky=True)
  latest_posts = Post.objects.filter(sticky=False).order_by('-published')[:5]
  latest_discussion = Comment.objects.all().order_by('-submit_date')[:5]
  return render_to_response('homepage.html', {
                                              'featured_posts': featured_posts,
                                              'latest_posts': latest_posts, 
                                              'latest_discussion' : latest_discussion, 
                                            }, context_instance = RequestContext(request))

def post(request):
  preview = "preview" in request.POST
  if preview:
    comment = request.POST.__getitem__('comment')
    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    comment = p.parse(comment).childNodes[0].childNodes[1].toxml()[6:-7]
    req = HttpRequest()
    req.path = request.path
    req.method = request.method
    req.encoding = request.encoding
    req.user = request.user
    req.session = request.session
    req.raw_post_data = request.raw_post_data
    #req.urlconf = request.urlconf
    req.FILES = request.FILES
    req.GET = request.GET
    req.COOKIES = request.COOKIES
    req.META = request.META
    req.POST = request.POST.copy()
    req.POST.__setitem__('comment', comment)
    
    return post_comment(req) 
  else:
    return post_comment(request)
