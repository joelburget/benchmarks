from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

def showuser(request, uname):
  user = get_object_or_404(User, username=uname)
  return render_to_response('users/showuser.html', {'object':user}, context_instance=RequestContext(request))
