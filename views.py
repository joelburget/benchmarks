from benchmarks.posts.models import Post
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.comments.models import Comment
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

def homepage(request):
  #featured posts always stay on the homepage
  featured_posts = Post.objects.filter(sticky=True)
  latest_posts = Post.objects.filter(sticky=False).order_by('-published')[:5]
  latest_discussion = Comment.objects.all().order_by('-submit_date')[:5]
  return render_to_response('homepage.html', {
                                              'featured_posts': featured_posts,
                                              'latest_posts': latest_posts, 
                                              'latest_discussion' : latest_discussion, 
                                              'less_style' : True,
                                            }, context_instance = RequestContext(request))

def loginuser(request):
  if request.method == 'POST':
    # Get post parameters
    u = request.POST['username']
    p = request.POST['password']
    user = authenticate(username = u, password = p)

    if user is not None and user.is_active:
      # Login, valid and active user
      lastpage = request.session['lastpage']
      login(request, user)
      return HttpResponseRedirect(lastpage)
    else:
      # Error! User isn't valid or account details are wrong
      return direct_to_template(request, 'login_invalid.html')
  else:
    # Login form accessed without using POST, just
    # redirect them to the homepage
    return HttpResponseRedirect('/')

def logoutuser(request):
  # Logout user
  lastpage = request.session['lastpage']
  logout(request)
  return HttpResponseRedirect(lastpage)


