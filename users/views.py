from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment

def showuser(request, uname):
  u = get_object_or_404(User, username=uname)
  posts = u.post_set.all()
  comments = Comment.objects.filter(user=u)
  return render_to_response('users/showuser.html', 
    context_instance=RequestContext(request, {
                                              'object' : u, 
                                              'posts' : posts,
                                              'comments_list' : comments
                                             }))
