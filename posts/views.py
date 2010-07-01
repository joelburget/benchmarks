from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, logout
from benchmarks.posts.models import Post, PostForm
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.template import RequestContext

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

def editpost(request):
  if request.method == 'POST': 
    print "posted"
    post = Post(author=request.user)
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
      print "valid"
      form.save()
      return HttpResponseRedirect('/')#should redirect to post
    else:
      print form.errors
  else:
    print "newform"
    form = PostForm()

  return render_to_response('posts/new_post.html', {
      'form': form,
  })
