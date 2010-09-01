from urllib import unquote

from benchmarks.posts.helpers import *
from benchmarks.posts.models import Post, PostForm, POSTTYPES
from benchmarks.templatetags.templatetags.date_diff import date_diff
from benchmarks.settings import SITE_ROOT

from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

@login_required
def editpost(request, post_id, **kwargs):
  if request.method == 'POST':
    # Update post
    post = get_object_or_404(Post, pk=post_id)
    status = update_post(post, request.POST, request.user)

    # Check status
    if status:
      # Check for files
      if request.FILES:
        for f in request.FILES:
          thisfile = request.FILES[f]
          pf = PostFile(file=thisfile)
          pf.save()

          # Associate it to the post
          post.files.add(pf)
          post.save()
          pf.file = thisfile
          pf.save()

          # Unzip
          zippath = os.path.join(SITE_ROOT, 'assets/') + str(pf.file)
          decompress(zippath, post)

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
                                'is_problem' : post.category == 'P',
                              },
                              context_instance=RequestContext(request))

@login_required
def newpost(request, **kwargs):
  # Check to make sure this is a POST request
  if request.method == 'POST':
    post = Post(author=request.user)
    status = new_post(post, request.POST)

    if status:
      post.up_to_date = True
      post.save()

      # Check for files
      if request.FILES:
        for f in request.FILES:
          thisfile = request.FILES[f]
          #pf = PostFile(file=thisfile, filetype='O')
          pf = PostFile(filetype='O')
          pf.save()

          # Associate it to the post
          post.files.add(pf)
          post.save()
          pf.file = thisfile
          pf.save()

          # Unzip
          zippath = os.path.join(SITE_ROOT, 'assets/') + str(pf.file)
          decompress(zippath, post)

        # Possibly this save should move down a level? I'm not sure.
        # It would result in less saves so less overhead but I'm not
        # sure they're that expensive, or if something could go wrong.
        # If we decide to change this, remember to change the one
        # above as well
        #post.save()

      # Success, render the post
      return HttpResponseRedirect("%s%s" % (post.get_absolute_url(), "created/"))
    else:
      # Failure, rerender the form page
      form = PostForm(instance = post)
      return render_to_response('posts/new_post.html', {'form' : form}, \
                                context_instance=RequestContext(request))
  else:
    # GET request, just render page w/o processing params
    problem = request.GET.get('problem', '')
    category = request.GET.get('category', '')
    form = PostForm()
    return render_to_response('posts/new_post.html', \
                              {
                                'form' : form,
                                'problem' : problem,
                                'category' : category,
                              }, \
                              context_instance=RequestContext(request))

def manage_files(request, post_id):
  if request.method == 'POST':
    return manage_files_post(request, post_id)
  else:
    return manage_files_get(request, post_id)

def manage_files_post(request, post_id):
  try:
    post = Post.objects.get(pk=post_id)
    if request.user != post.author:
      return HttpResponseRedirect('/')
    else:
      for (key,value) in request.POST.items():
        if key != "csrfmiddlewaretoken":
          if value[:3] == "vcs":
            f = PostFile.objects.get(pk=value[3:])
            f.filetype = 'V'
          elif value[:4] == "code":
            f = PostFile.objects.get(pk=value[4:])
            f.filetype = 'C'
          elif value[:5] == "specs":
            f = PostFile.objects.get(pk=value[5:])
            f.filetype = 'S'
          else:
            f = PostFile.objects.get(pk=value[5:])
            f.filetype = 'O'
          f.save()
      return HttpResponseRedirect(post.get_absolute_url())
  except Exception:
    return HttpResponseRedirect('/')

def manage_files_get(request, post_id):
  try:
    post = Post.objects.get(pk=post_id)
    if request.user != post.author:
      return HttpRespnseRedirect('/')
    return render_to_response('posts/manage_files.html', {'files': post.files}, context_instance=RequestContext(request))
  except Exception as e:
    print e
    return HttpResponseRedirect('/')

def index(request):
  userlist = User.objects.all()

  if 'searchtxt' in request.GET:
    searchtxt = request.GET['searchtxt']

    # Get categories
    categories = []

    for t in POSTTYPES:
      code, category = t

      if category.lower() in request.GET:
        categories.append(code)

    # Get advanced text fields
    title = request.GET.get('title', '')
    body = request.GET.get('body', '')
    user = request.GET.get('user', '')

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
      #This throws a syntax error for me.
      #userq = ~Q(pk=0))
      pass
    else:
      u = userlist.filter(username=user)
      userq = Q(author=u)

    # Check for advanced query
    # i.e. textfield, bodyfield, or less than the amount of post types we have
    advanced_submitted = len(categories) < len(POSTTYPES) or title != '' or body != '' or user != ''

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
      's' : 'S' in categories, 
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
  if request.is_ajax():
    return render_to_response('posts/post.html', { 'object' : post })
  else:
    return render_to_response('posts/post_detail.html', 
        { 'object' : post }, 
        context_instance=RequestContext(request))

def revision_info(request, post_id, post_history_id, **kwargs):
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
      return HttpResponse('ERROR: Bad history object [info].')

    post = PostRevision.objects.get(pk=post_history_id)

  # Return the post
  response = "<strong>by </strong> %s %s" % (post.author, date_diff(post.published),)
  return HttpResponse(response)

def created(request, post_id):
  post = Post.objects.get(pk=post_id)
  if request.method != 'POST':
    if not post.files.all():
      return HttpResponseRedirect(post.get_absolute_url())
    else:
      return direct_to_template(request, 'posts/created.html', {'post_id': post_id})

  else:
    if 'see' in request.POST.keys():
      #temporary - change the others too!
      return HttpResponseRedirect(post.get_absolute_url())
    else:
      return HttpResponseRedirect("%smanage_files/" % post.get_absolute_url())
  return render_to_response('posts/categorize.html', context_instance=RequestContext(request))

def detail(request, object_id):
  # Get object
  object = Post.objects.get(pk=object_id)

  # Get Revision
  rev = None
  if request.method == 'GET':
    rev = request.GET.get('revision', None)

  if rev != None and rev != 'original':
    revision = PostRevision.objects.get(pk=rev)
  else:
    revision = None

  # Render response
  return render_to_response('posts/post_detail.html', {'object' : object, 'revision' : revision},
    context_instance=RequestContext(request))
