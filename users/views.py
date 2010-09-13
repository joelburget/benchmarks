from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.contrib.auth.models import User
from benchmarks.extended_comments.models import ExtendedComment
from benchmarks.helpers import *
from benchmarks.helpers import *
from benchmarks.users.forms import *
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def index(request):
  if 'searchtxt' in request.GET:
    searchtxt = request.GET['searchtxt']
    pusers = User.objects.filter(
      Q(username__icontains=searchtxt) | 
      Q(first_name__icontains=searchtxt) |
      Q(last_name__icontains=searchtxt) 
    ).distinct()
  else:
    searchtxt = ''
    pusers = User.objects.all()

  users = get_page_of_objects(pusers, request) 
  return render_to_response('users/index.html', 
    context_instance=RequestContext(request, { 'searchtxt' : searchtxt, 'users' : users}))

def showuser(request, uname):
  u = get_object_or_404(User, username=uname)
  posts = u.post_set.all()[:5]
  comments = ExtendedComment.objects.filter(user=u).order_by('-published')[:5]
  return render_to_response('users/showuser.html', 
    context_instance=RequestContext(request, {
                                              'object' : u, 
                                              'posts' : posts,
                                              'comments_list' : comments
                                             }))

def edituser(request, uname):
  person = get_object_or_404(User, username=uname)
  me = request.user

  if me.is_authenticated() == False or person != me:
    # Incorrect permissions
    return redirect_to_error(403, 'You don\'t have permission!')

  if request.method == 'POST':
    # Save incoming data
    profile_form = UserProfileForm(request.POST, instance = me.get_profile())
    user_form = UserForm(request.POST, instance = me)

    profile_form.save()
    user_form.save()

    return HttpResponseRedirect(me.get_absolute_url())
  else:
    # Display form
    dict = {
      'profile_form' : UserProfileForm(instance = me.get_profile()),
      'user_form' : UserForm(instance=me)
    }
    return render_to_response('users/edit.html', dict, context_instance=RequestContext(request))
