from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, logout
from benchmarks.posts.models import Post
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.template import RequestContext

def post_detail(request, object_id):
  p = get_object_or_404(Post, pk=object_id)
  return render_to_response('posts/post_detail.html', {'object':p, 'user':request.user}, context_instance=RequestContext(request))

def loginuser(request):
  if request.method == 'POST':
    # Get post parameters
    u = request.POST['username']
    p = request.POST['password']
    user = authenticate(username = u, password = p)

    if user is not None and user.is_active:
      # Login, valid and active user
      login(request, user)
      return HttpResponseRedirect('/1/')
    else:
      # Error! User isn't valid or account details are wrong
      return direct_to_template(request, 'login_invalid.html')

def logoutuser(request):
  # Logout user and open up the logout screen
  logout(request)
  return direct_to_template(request, 'logout.html')

