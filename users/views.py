from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from benchmarks.users.models import UserForm 
from django.http import HttpResponseRedirect

def showuser(request, uname):
  u = get_object_or_404(User, username=uname)
  posts = u.post_set.all()
  comments = Comment.objects.filter(user=u).order_by('-submit_date')[:10]
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
      meform.save()
      return HttpResponseRedirect('/user/' + me.username + '/')
    else:
      # Display form
      formset = UserForm(instance=me)
      return render_to_response('users/edituser.html',
        context_instance=RequestContext(request, { 'formset' : formset, }))
  else:
    # Disallow edits
    return direct_to_template(request, 'users/edituser_bad.html')
