from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

def showuser(request, uname):
  u = get_object_or_404(User, username=uname)
  posts = u.post_set.all()
  return render_to_response('users/showuser.html', context_instance=RequestContext(request, {'object':u, 'posts':posts}))
