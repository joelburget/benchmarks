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
from django.views.generic.simple import direct_to_template 
from django.views.decorators.http import require_POST

def homepage(request):
  # Grab all problems, all non-problems, and all comments
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
  # Logout user
  logout(request)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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

@require_ajax
def dirlist(request):
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
  return RssPostsFeed().__call__(request)

def atom(request):
  return AtomPostsFeed().__call__(request)

@require_POST
def joined(request):
  if settings.EMAIL_ENABLED:
    # Generate email message from post params
    name = request.POST['name']
    username = name.lower().replace(' ', '')
    email = request.POST['email']
    group = request.POST['group']
    reason = request.POST['reason']

    # Send message
    email = EmailMessage('Intent to Join - %s' % (name,),
      "==========================================\n" \
      "Intent to Join Software Benchmarks Website\n" \
      "==========================================\n" \
      "\n" \
      "Username: %s\n" \
      "Real Name: %s\n" \
      "Email Address: %s\n" \
      "Research Organization: %s\n" \
      "Information: %s\n" \
      "\n" \
      "To allow this user to join, click here:\n" \
      "http://%s/user-create/?username=%s&realname=%s&email=%s\n" \
        % ((username, name, email, group, reason, settings.SITE_URL) + \
          tuple(map(urllib.quote_plus, (username, name, email)))), \
      to=[settings.ADMIN_EMAIL])

    # Send message
    email.send()

  return render_to_response('users/joined.html', context_instance=RequestContext(request))

def user_create(request):
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
      'Welcome! You\'re account has been set up at the OSU Benchmarks' \
      ' website!\n\n' \
      'Username: %s\n' \
      'Password: %s\n\n' \
      'Open up http://%s/ in your browser, and enter your info into the side' \
      ' panel to get started!' % (username, password, settings.SITE_URL),
      to=[email])

    email.send()

    # Confirmation message
    return HttpResponse('OK! %s\'s account was created! An automated ' \
                          'email was sent to him/her...' % (username,))

  # Error
  return HttpResponse('You don\'t have access to do this! Please log in or kindly leave!')
