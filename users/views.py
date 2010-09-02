from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.contrib.auth.models import User
from benchmarks.extended_comments.models import ExtendedComment
from benchmarks.helpers import *
from benchmarks.users.forms import UserForm 
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
  # Get the users wanted to edit, and the current user
  wanteduser = get_object_or_404(User, username=uname)
  me = request.user

  # Ensure that the user editing this profile is allowed (i.e. the
  # user and the profile are the same person)
  if wanteduser.username == me.username:
    # Allow edits
    if request.method == 'POST':
      # Save changes
      meform = UserForm(request.POST, instance=me)

      if meform.is_valid():      
        # Save form
        meform.save()

        # Hack for profiles
        profile = me.get_profile()
        profile.bio = request.POST.get('bio', '')

        profile.showemail = ('showemail' in request.POST) or False
        profile.commentResponseSubscribe = ('commentResponseSubscribe' in request.POST) or False
        profile.ownPostCommentSubscribe = ('ownPostCommentSubscribe' in request.POST) or False
        profile.groupPostSubscribe = ('groupPostSubscribe' in request.POST) or False
        profile.allProblemSubscribe = ('allProblemSubscribe' in request.POST) or False
        profile.save()

        return HttpResponseRedirect(me.get_absolute_url())
      else:
        # Redisplay with errors
        return render_to_response('users/edituser.html',
          context_instance=RequestContext(request, { 'formset' : meform, }))
    else:
      # Display form
      formset = UserForm(instance=me)
      return render_to_response('users/edituser.html',
        context_instance=RequestContext(request, { 'formset' : formset, }))
  else:
    # Disallow edits
    return direct_to_template(request, 'users/edituser_bad.html')
