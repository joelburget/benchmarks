import re
import os
import urllib
from benchmarks.settings import SITE_ROOT
from benchmarks.posts.models import Post
from benchmarks.extended_comments.models import ExtendedComment
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.simple import direct_to_template 
from django.http import Http404

def homepage(request):
  # featured posts always stay on the homepage
  featured_posts = Post.objects.filter(sticky=True)
  latest_posts = Post.objects.filter(sticky=False).order_by('-published')[:5]
  latest_discussion = ExtendedComment.objects.all().order_by('-submit_date')[:5]
  return render_to_response('homepage.html', {
                                              'featured_posts': featured_posts,
                                              'latest_posts': latest_posts, 
                                              'latest_discussion' : latest_discussion, 
#                                              'less_style' : True,
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

def our404(request, error='404'):
  # Get path
  path = request.get_full_path()

  # Apply regex to find url
  if re.match('/posts/[0-9]*/', path):
    # Post
    suggestion = '<li>Take a look at all of the <a href="/posts">posts</a> on our site.</li>'
  elif re.match('/users/.*/', path):
    # User
    suggestion = '<li>Take a look at all of the users on our site.</li>'
  elif re.match('/groups/.*/', path):
    # Group
    suggestion = '<li>Take a look at all of the <a href="/groups">groups</a> on our site.</li>'
  else:
    suggestion = ''

  # Determine error type
  if error == '404':
    msg = 'Uh oh!  We\'re sorry, but the page you tried to access doesn\'t exist!'
  else:
    msg = 'Uh oh!  Something funky went on with our server!'

  return render_to_response('404.html', {'msg' : msg, 'suggestion' : suggestion})

def our500(request):
  return our404(request, error='500') 

# Modified connector script for Django from jqueryFileTree codebase
def dirlist(request):
   if not request.is_ajax():
     raise Http404
   r=['<ul class="jqueryFileTree" style="display: none;">']
   try:
       r=['<ul class="jqueryFileTree" style="display: none;">']
       uploads = os.path.join(SITE_ROOT, 'assets/uploads/')
       d=urllib.unquote(request.POST.get('dir', '/'))

       if d[0] != '/': d = uploads + d

       for f in os.listdir(d):
           ff=os.path.join(d,f)
           if os.path.isdir(ff):
               r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
           else:
               e=os.path.splitext(f)[1][1:] # get .ext and remove dot
               r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
       r.append('</ul>')
   except Exception,e:
       r.append('Could not load directory: %s' % str(e))
   r.append('</ul>')
   return HttpResponse(''.join(r))
