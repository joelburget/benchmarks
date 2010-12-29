from urllib import unquote

from benchmarks.helpers import *
from benchmarks.posts.helpers import *
from benchmarks.posts.models import Post, POSTTYPES, FILETYPES
from benchmarks.posts.forms import PostForm
from benchmarks.templatetags.templatetags.date_diff import date_diff
from benchmarks.settings import SITE_ROOT
from benchmarks.markdown2 import markdown

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

      # Convert to markdown then replace TeX with images
      post.body_display = markdown(post.body)
      post.save()
      post.render_equations()

      # Redirect to post
      return HttpResponseRedirect(post.get_absolute_url())
    else:
      # Failure, rerender the form page
      form = PostForm(instance = post)
      return render_to_response('posts/new_post.html', 
                                {'form' : form, 'edit': True },
                                context_instance=RequestContext(request))
  else: # request.method == 'GET'
    # Display edit form for post
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=post)
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

      # Convert to markdown then replace TeX with images
      post.body_display = markdown(post.body)
      post.save()
      post.render_equations()

      # Success, render the post
      return HttpResponseRedirect("%s%s" % (post.get_absolute_url(), 
                                  "created/"))
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
    return render_to_response('posts/manage_files.html', \
      {'files': post.files}, context_instance=RequestContext(request))
  except Exception as e:
    return HttpResponseRedirect('/')

def index(request):
  userlist = User.objects.all()

  if not 'searchtxt' in request.GET:
    # No searching, just render a paginated view of all posts
    posts = get_page_of_objects(Post.objects.all().order_by('-published'), \
                                request)
    return render_to_response('posts/index.html', \
                              { 'posts':posts, 'userlist' : userlist }, \
                              context_instance=RequestContext(request))
  else:
    # Search performed
    searchtxt = request.GET['searchtxt']  # main search textbox
    title = request.GET.get('title', '')  # advanced -title of post
    body = request.GET.get('body', '')    # advanced - body of post
    user = request.GET.get('user', '')    # advanced - author

    categories = []                       # get categories selected
    for t in POSTTYPES:
      code, category = t
      if category.lower() in request.GET:
        categories.append(code)

    # Determine text search required
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
    # i.e. textfield, bodyfield, or less than the amount of post types we have
    advanced_submitted = len(categories) < len(POSTTYPES) \
                         or title != '' or body != '' or user != ''

    # Advanced query
    pposts = Post.objects.filter(
      text, 
      userq,
      category__in=categories
    ).distinct().order_by('-published')

    # Render
    posts = get_page_of_objects(pposts, request)
    return render_to_response('posts/index.html', {
      'searchtxt' : searchtxt,
      'posts' : posts,
      'title' : title,
      'body' : body,
      'u' : user,
      'userlist' : userlist,
      'p' : 'P' in categories, 
      's' : 'S' in categories, 
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

    #post = PostRevision.objects.get(pk=post_history_id)

  # Return the post
  if request.is_ajax():
    return render_to_string('partials/post_full.html', { 'item' : post })
  else:
    return render_to_response('posts/post_detail.html', 
        { 'object' : post }, 
        context_instance=RequestContext(request))

def created(request, post_id):
  post = Post.objects.get(pk=post_id)
  if request.method != 'POST':
    if not post.files.all():
      return HttpResponseRedirect(post.get_absolute_url())
    else:
      return direct_to_template(request, 
                                'posts/created.html', 
                                {'post_id': post_id})

  else:
    if 'see' in request.POST.keys():
      #temporary - change the others too!
      return HttpResponseRedirect(post.get_absolute_url())
    else:
      return HttpResponseRedirect("%smanage_files/" % post.get_absolute_url())
  return render_to_response('posts/categorize.html', 
                            context_instance=RequestContext(request))

def detail(request, object_id):
  # Get object
  object = Post.objects.get(pk=object_id)


  # Get Revision
  rev = None
  if request.method == 'GET':
    rev = request.GET.get('revision', None)

  if rev != None and rev != 'original':
    pass
		#revision = PostRevision.objects.get(pk=rev)
  else:
    revision = None

  # Render response
  return render_to_response('posts/post_detail.html', {'object' : object, 'revision' : revision},
    context_instance=RequestContext(request))

@login_required
def new(request):
  if request.method == 'GET':
    if request.user.get_profile().group == None:
      # No group error
      return redirect_to_error(403, 'You need to join a group before posting!')
    else:
      # Render basic new post page
      return direct_to_template(request, 'posts/new.html', {
                                  'category' : request.GET.get('category', 'P'),
                                  'problem' : request.GET.get('problem', '')})
  else:
    # Create a new post
    title = request.POST.get('title')
    category = request.POST['category'] if 'category' in request.POST else 'P'
    pk = request.POST['problem'].isdigit()
    problem = Post.objects.get(pk=int(request.POST['problem'])) if pk else None

    post = Post(title = title,
                problem = problem,
                category = category, 
                author = request.user, 
                group = request.user.get_profile().group)
    post.save()
    return HttpResponseRedirect('/posts/%s/upload/' % post.pk)

@login_required
def upload(request, post_id):
  post = get_object_or_404(Post, pk=post_id)

  if request.method == 'GET':
    if post.group == request.user.get_profile().group:
      # Render form
      return direct_to_template(request, 'posts/upload.html', {'post':post})
    else:
      # Incorrect permissions
      return redirect_to_error(403, '')    
  else:
    # Associate uploaded files with this post
    for f in request.FILES:
      file = PostFile(file = request.FILES[f], filetype = 'O')
      file.save()
      post.files.add(file)

      zippath = os.path.join(SITE_ROOT, 'assets/') + str(file.file)
      decompress(zippath, post)

    post.save()

    # Redirect to either the file management interface or the description editor
    if request.FILES:
      return HttpResponseRedirect('/posts/%s/manage/' % post.pk)
    else:
      return HttpResponseRedirect('/posts/%s/description/' % post.pk)

@login_required
def manage(request, post_id):
  post = get_object_or_404(Post, pk=post_id)

  if request.method == 'GET':
    if post.group == request.user.get_profile().group:
      # Render form
      return direct_to_template(request, 'posts/manage_files.html', {'post' : post}) 
    else:
      # Incorrect permissions
      return redirect_to_error(403, '')
  else:
    # Update filetypes for all files associated with this post
    for key in request.POST:
      value = request.POST[key]

      if key != 'csrfmiddlewaretoken':
        # e.g. value = 'code3'
        # pk = '3'
        # type = 'code'
        pk = key.replace("group", "")

        if "input" in value:
          type = "N"
        elif "output" in value:
          type = "U"
        elif "other" in value:
          type = "O"

        file = PostFile.objects.get(pk=pk)
        file.filetype = type
        file.save()

    return HttpResponseRedirect('/posts/%s/description/' % post.pk)

@login_required
def description(request, post_id):
  post = get_object_or_404(Post, pk=post_id)

  if request.method == 'GET':
    if post.group == request.user.get_profile().group:
      # Render form
      ftypes = set()
      for file in post.files.all():
        ftypes.add(file.get_filetype_display())

      return direct_to_template(request, 'posts/describe.html', {'post':post, 'ftypes':ftypes})
    else:
      # Incorrect permissions
      return redirect_to_error(403, '')
  else:
    # Update text
    post.body = request.POST['body']
    post.save()

    # Convert to markdown then replace TeX with images
    post.body_display = markdown(post.body)
    post.save()
    post.render_equations()

    return HttpResponseRedirect(post.get_absolute_url())
