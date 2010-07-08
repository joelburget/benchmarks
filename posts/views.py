import os
from django.shortcuts import get_object_or_404, render_to_response
from benchmarks.posts.models import Post, PostForm, PostFile
from benchmarks.posts.helpers import *
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.template import RequestContext

def editpost(request):
  # Only authenticated users may post
  if not request.user.is_authenticated():
    # Error! Must login...
    return direct_to_template(request, 'posts/must_login.html')
  if request.method == 'POST': 
    # Get POST data for new post
    post = Post(author=request.user)
    form = PostForm(request.POST, instance=post)

    if form.is_valid():
      # Save post
      form.save()
      
      # Save files in uploads/ and in db
      for f in request.FILES:
        thisfile = request.FILES[f]
        handle_uploaded_file(thisfile, post.pk)

        pf = PostFile(file = thisfile, post = post)
        pf.save()

      # Redirect to the submitted post
      return HttpResponseRedirect(post.get_absolute_url())
  else:
    # Get a blank post form for editing
    form = PostForm()

  return render_to_response('posts/new_post.html', { 'form': form }, context_instance=RequestContext(request))


def search(request):
  if request.method == 'POST':
    # Display search form and results
    query = request.POST['query']
    hits = Post.objects.filter(body__icontains=query)
  else:
    # Just display search form
    query = ''
    hits = []

  return render_to_response('posts/search.html', {'query' : query, 'hits' : hits},
    context_instance=RequestContext(request))
