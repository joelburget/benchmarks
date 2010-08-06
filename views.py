import os
import re
import urllib

from benchmarks import settings
from benchmarks.extended_comments.models import ExtendedComment
from benchmarks.feeds import RssPostsFeed, AtomPostsFeed
from benchmarks.helpers import *
from benchmarks.posts.models import Post

from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template 

def homepage(request):
  # Grab all problems, all non-problems, and all comments
  problem_posts = Post.objects.filter(category='P')[:3]
  latest_posts = Post.objects.exclude(category='P').order_by('-published')[:3]
  latest_discussion = ExtendedComment.objects.all().order_by('-submit_date')[:3]
  return render_to_response('homepage.html',
                            {
                              'problem_posts': problem_posts,
                              'latest_posts': latest_posts, 
                              'latest_discussion' : latest_discussion, 
                            },
                            context_instance = RequestContext(request))

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

def dirlist(request):
  response = '<ul class="jqueryFileTree" style="display:none;">\n'

  if request.is_ajax():
    if 'dir' in request.POST:
      # Get directory
      root = os.getcwd() + request.POST['dir']
      l = generate_dirs_list(root)
      response += l
    else:
      # No "dir" parameter
      response += 'Error! A "dir" GET parameter is required to access this URL.'
  else:
    # Non-POST methods
    response += 'Error! This URL can only be accessed with a POST method.'

  response += '</ul>'
  return HttpResponse(response)

def rss(request):
  return RssPostsFeed().__call__(request)

def atom(request):
  return AtomPostsFeed().__call__(request)

def joined(request):
  if request.method == 'POST' and settings.EMAIL_ENABLED:
    # Generate email message from post params
    name = request.POST['name']
    email = request.POST['email']
    group = request.POST['group']
    reason = request.POST['reason']

    email = EmailMessage('Intent to Join ',
"""
==========================================
Intent to Join Software Benchmarks Website
==========================================

Real Name: %s
Email Address: %s
Research Organization: %s
Rationale: %s

To allow this user to join, click here:
http://fixme.com
""" % (name, email, group, reason),
      to=['weide.1@osu.edu'])

    # Send message
    email.send()
  else:
    print 'Emailing disabled! Not sending account registration!'

  return render_to_response('users/joined.html')
