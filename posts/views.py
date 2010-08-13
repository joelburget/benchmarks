from urllib import unquote

from benchmarks.posts.helpers import *
from benchmarks.posts.models import CATEGORY_CHOICES
from benchmarks.posts.models import Post, PostForm

from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template

def editpost(request, post_id, **kwargs):
  if not request.user.is_authenticated():
    return direct_to_template(request, 'posts/must_login.html')

  if request.method == 'POST':
    # Update post
    post = get_object_or_404(Post, pk=post_id)
    status = update_post(post, request.POST)

    # Check status
    if status:
      # Redirect to post
      return HttpResponseRedirect(post.get_absolute_url())
    else:
      # Failure, rerender the form page
      form = PostForm(instance = post)
      return render_to_response('posts/new_post.html', {'form' : form, 'edit': True }, \
                                context_instance=RequestContext(request))
  else:
    # Display edit form for post
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance = post)
    return render_to_response('posts/new_post.html',
                              {
                                'form' : form,
                                'edit' : True,
                              },
                              context_instance=RequestContext(request))

def newpost(request, **kwargs):
  if not request.user.is_authenticated():
    # Require the user to be logged in
    return direct_to_template(request, 'posts/must_login.html')

  # Check to make sure this is a POST request
  if request.method == 'POST':
    post = Post(author=request.user)
    status = new_post(post, request.POST)

    if status:
      # Success, render the post
      return HttpResponseRedirect(post.get_absolute_url())
    else:
      # Failure, rerender the form page
      form = PostForm(instance = post)
      return render_to_response('posts/new_post.html', {'form' : form}, \
                                context_instance=RequestContext(request))
  else:
    # GET request, just render page w/o processing params
    parent = request.GET.get('parent', '')
    category = request.GET.get('category', '')
    form = PostForm()
    return render_to_response('posts/new_post.html', \
                              {
                                'form' : form,
                                'parent' : parent,
                                'category' : category,
                              }, \
                              context_instance=RequestContext(request))

def index(request):
  userlist = User.objects.all()

  if 'searchtxt' in request.GET:
    searchtxt = request.GET['searchtxt']

    # Get categories
    categories = []

    for t in CATEGORY_CHOICES:
      code, category = t

      if category.lower() in request.GET:
        categories.append(code)

    # Get advanced text fields
    title = request.GET.get('title', '')
    body = request.GET.get('body', '')

    user = request.GET.get('user', '')
    #featured = request.GET.get('featured', '')

    if title != '' and body != '':
      text = Q(title__icontains=title) & Q(body__icontains=body)
    elif title != '' and body == '':
      text = Q(title__icontains=title)
    elif title == '' and body != '':
      text = Q(body__icontains=body)
    else:
      text = Q(title__icontains=searchtxt) | Q(body__icontains=searchtxt)

    if user == '':
      # Ugly hack
      userq = ~Q(pk=0)
    else:
      u = userlist.filter(username=user)
      userq = Q(author=u)

    # Check for advanced query
    # i.e. textfield, bodyfield, or less than the 4 default checkboxes
    advanced_submitted = len(categories) < 4 or title != '' or body != '' or user != ''

    # Advanced query
    pposts = Post.objects.filter(
      text, 
      userq,
      category__in=categories
    ).distinct().order_by('-published')
  else:
    advanced_submitted = False
    user = ''
    title = ''
    body = ''
    categories = []
    searchtxt = ''
    pposts = Post.objects.all().order_by('-published')

  paginator = Paginator(pposts, 10)

  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    posts = paginator.page(page)
  except (EmptyPage, InvalidPage):
    posts = paginator.page(paginator.num_pages)

  return render_to_response('posts/index.html', {
      'searchtxt' : searchtxt,
      'posts' : posts,
      'title' : title,
      'body' : body,
      'u' : user,
      'userlist' : userlist,
      'p' : 'P' in categories, 
      'r' : 'R' in categories, 
      'v' : 'V' in categories, 
      'o' : 'O' in categories, 
      'advanced_submitted' : advanced_submitted,
    },
    context_instance=RequestContext(request))

def posthistory(request, post_id, post_history_id, **kwargs):
  post = None

  if post_history_id == 'original':
    # Grab original post
    post = Post.objects.get(pk=post_id)
  else:
    # Grab a post history object
    rev_pk = 0

    try:
      rev_pk = int(post_history_id)
    except:
      return HttpResponse('ERROR: Bad history object.')

    post = PostRevision.objects.get(pk=post_history_id)

  # Return the post
  return render_to_response('posts/post.html', { 'object' : post })

def revision_info(request, post_id, post_history):
  if request.is_ajax():
    # Get main post
    post = Post.objects.get(pk=post_id)

    # Get history
    hist = post.history()
   
    for revision in hist: 
      if str(revision) == unquote(post_history_id):
        return HttpResponse(serializers.serialize('json', revision))

    return HttpResponse('ERROR: Bad history object.') 
