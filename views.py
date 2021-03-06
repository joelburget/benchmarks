import os
import random
import re
import urllib

from benchmarks import settings
from benchmarks.extended_comments.models import ExtendedComment
from benchmarks.feeds import RssPostsFeed, AtomPostsFeed
from benchmarks.helpers import *
from benchmarks.posts.models import Post
from benchmarks.decorators import require_ajax

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic.simple import direct_to_template 
from django.views.decorators.http import require_POST

def homepage(request):
  """
  Homepage view
  Displays latest problems, solutions, and discussion
  """
  problem_posts = Post.objects.filter(category='P').order_by('-published')[:3]
  latest_posts = Post.objects.filter(category='S').order_by('-published')[:3]
  latest_discussion = ExtendedComment.objects.all().order_by('-published')[:3]

  return render_to_response('homepage.html',
                            {
                              'problem_posts': problem_posts,
                              'latest_posts': latest_posts, 
                              'latest_discussion' : latest_discussion, 
                            },
                            context_instance = RequestContext(request))

@require_POST
def loginuser(request):
  """
  Wrapper for authenticate/login function from django.contrib.auth
  Returns user to the last page they viewed, or the homepage.
  """
  if request.method == 'POST':
    # Get post parameters
    u = request.POST['username']
    p = request.POST['password']
    user = authenticate(username = u, password = p)

    if user is not None and user.is_active:
      # Login, valid and active user
      login(request, user)
      return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
      # Error! User isn't valid or account details are wrong
      return direct_to_template(request, 'login_invalid.html')

def logoutuser(request):
  """
  Wrapper for logout function from django.contrib.auth
  Returns user to the last page they viewed, or the homepage.
  """
  logout(request)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def our404(request):
  """
  404 Error - custom view for production mode
  """
  return redirect_to_error(404, 'This page doesn\'t exist.')

def our500(request):
  """
  500 Error - custom view for production mode
  """
  return redirect_to_error(500, 'Something in our server broke. Please try again later.')

@require_ajax
def dirlist(request):
  """
  Generates a directory list, used for the JQuery filebrowser
  """
  response = '<ul class="jqueryFileTree" style="display:none;">\n'

  if 'dir' in request.POST:
    # Get directory
    root = os.getcwd() + request.POST['dir']
    l = generate_dirs_list(root)
    response += l
  else:
    # No "dir" parameter
    response += 'Error! A "dir" POST parameter is required to access this URL.'

  response += '</ul>'
  return HttpResponse(response)

def rss(request):
  """
  RSS Feed
  """
  return RssPostsFeed().__call__(request)

def atom(request):
  """
  Atom Feed
  """
  return AtomPostsFeed().__call__(request)

@require_POST
def joined(request):
  """
  User account request view
  Sends an autogenerated email to them
  """
  if settings.EMAIL_ENABLED:
    # Generate email message from post params
    name = request.POST['name']
    username = name.lower().replace(' ', '')
    email = request.POST['email']
    group = request.POST['group']
    reason = request.POST['reason']
    url = '%s/user-create/?username=%s&realname=%s&email=%s' % ((settings.SITE_URL,) + tuple(map(urllib.quote_plus, (username, name, email))))

    # Send message
    email = EmailMessage('Intent to Join - %s' % name,
                         render_to_string('emails/user_request.txt',
                           {
                             'name' : name,
                             'email' : email,
                             'group' : group,
                             'reason' : reason,
                             'url' : url
                           }),
                         to=[settings.ADMIN_EMAIL])

    # Send message
    email.send()

  return render_to_response('users/joined.html', context_instance=RequestContext(request))

def user_create(request):
  """
  Creates a user account
  To be used by admins in autogenerated emails
  """
  if request.user.is_authenticated() and request.user.is_staff:
    # Generate random password
    random.seed()
    password = ''.join(random.sample(map(chr, \
                 range(ord('A'), ord('Z') + 1) + \
                 range(ord('a'), ord('z') + 1) + \
                 range(ord('0'), ord('9') + 1)), 8)) 

    # Create user object
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    u = User(username = username, email = email)
    u.set_password(password)
    u.save()

    # Send acceptance email to user
    email = EmailMessage('Welcome! - OSU Benchmarks Website',
      render_to_string('emails/user_created.txt', 
                       {
                         'username' : username,
                         'password' : password,
                         'url' : settings.SITE_URL
                       }),
                       to=[email])

    email.send()

    # Confirmation message
    return HttpResponse('OK! %s\'s account was created! An automated ' \
                          'email was sent to him/her...' % (username,))

  # Error
  return HttpResponse('You don\'t have access to do this! Please log in or kindly leave!')
