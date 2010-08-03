from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from benchmarks.users.models import UserForm 
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

  # Paginate
  paginator = Paginator(pusers, 10)
  
  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    users = paginator.page(page)
  except (EmptyPage, InvalidPage):
    users = pageinator.page(paginator.num_pages)

  return render_to_response('users/index.html', 
    context_instance=RequestContext(request, { 'searchtxt' : searchtxt, 'users' : users}))

def showuser(request, uname):
  u = get_object_or_404(User, username=uname)
  posts = u.post_set.all()[:5]
  comments = Comment.objects.filter(user=u).order_by('-submit_date')[:5]
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
        profile.bio = request.POST['bio'][0:200] # truncated to 200 chars

        if 'showemail' in request.POST:
          profile.showemail = True
        else:
          profile.showemail = False  # By HTML spec, nonchecked boxes don't go thru POST
        if 'commentResponseSubscribe' in request.POST:
          profile.commentResponseSubscribe = True
        else:
          profile.commentResponseSubscribe = False

        if 'ownPostCommentSubscribe' in request.POST:
          profile.ownPostCommentSubscribe = True
        else:
          profile.ownPostCommentSubscribe = False

        if 'groupPostSubscribe' in request.POST:
          profile.groupPostSubscribe = True
        else:
          profile.groupPostSubscribe = False

        if 'allProblemSubscribe' in request.POST:
          profile.allProblemSubscribe = True
        else:
          profile.allProblemSubscribe = False

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
