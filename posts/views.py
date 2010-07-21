import os
from datetime import datetime
import zipfile
from benchmarks.posts.models import CATEGORY_CHOICES
from django.shortcuts import get_object_or_404, render_to_response
from benchmarks.posts.models import Post, PostForm, PostFile
from benchmarks.posts.helpers import *
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from benchmarks.settings import SITE_ROOT
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def editpost(request):
  # Only authenticated users may post
  if not request.user.is_authenticated():
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
        pf = PostFile(file = thisfile, post = post)
        pf.save()

        # Check zips, tars, etc.
        zippath = os.path.join(SITE_ROOT, 'assets/') + str(pf.file)
        decompress(zippath, post)

      # Redirect to the submitted post
      return HttpResponseRedirect(post.get_absolute_url())
  else:
    # Get a blank post form for editing
    form = PostForm()

  return render_to_response('posts/new_post.html', { 'form': form }, context_instance=RequestContext(request))

def index(request):
  if 'searchtxt' in request.GET:
    searchtxt = request.GET['searchtxt']

    # Advanced search
    categories = []

    for t in CATEGORY_CHOICES:
      code, category = t

      if category.lower() in request.GET:
        categories.append(code)

    pposts = Post.objects.filter(
      Q(title__icontains=searchtxt) |
      Q(body__icontains=searchtxt), 
      category__in=categories
    ).distinct()
  else:
    categories = []
    searchtxt = ''
    pposts = Post.objects.all()

  paginator = Paginator(pposts, 10)

  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    posts = paginator.page(page)
  except (EmptyPage, InvalidPage):
    posts = paginator.page(paginator.num_pages)

  if len(categories) > 0:
    categories_submitted = True
  else:
    categories_submitted = False

  return render_to_response('posts/index.html', {
      'searchtxt' : searchtxt,
      'posts' : posts,
      'p' : 'P' in categories, 
      'r' : 'R' in categories, 
      'v' : 'V' in categories, 
      'o' : 'O' in categories, 
      'categories_submitted' : categories_submitted
    },
    context_instance=RequestContext(request))
