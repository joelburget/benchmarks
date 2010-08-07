from benchmarks.extended_comments.models import ExtendedComment
from benchmarks.extended_comments.forms import ExtendedCommentForm
from django.http import HttpRequest
import html5lib
from html5lib import sanitizer
import os
from benchmarks.settings import MEDIA_ROOT
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from benchmarks.posts.models import Post
from django.views.decorators.http import require_POST

#This sanitizes the input the user will see in the preview area for comments
#because that is not covered by the sanitization in comment-sanitizer/__init__.py
#(We want them to see what will actually show up)
@require_POST
def post(request):
  print request.POST
  if request.FILES:
    form = ExtendedCommentForm(request.POST, request.FILES)
    if form.is_valid():
      handle_uploaded_file(request.FILES['file'])
  preview = "preview" in request.POST
  #If the user is requesting a preview we must sanitize the input
  #The other option is if they are actually posting in which case
  #the input will already be sanitized
  if preview:
    comment = request.POST.__getitem__('comment')
    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    comment = p.parse(comment).childNodes[0].childNodes[1].toxml()[6:-7]
	
	#reqest.POST is immutable so we must create a new request to change request.POST
    req = HttpRequest()
    req.path = request.path
    req.method = request.method
    req.encoding = request.encoding
    req.user = request.user
    req.session = request.session
    req.raw_post_data = request.raw_post_data
    #req.urlconf = request.urlconf
    req.FILES = request.FILES
    req.GET = request.GET
    req.COOKIES = request.COOKIES
    req.META = request.META
    req.POST = request.POST.copy()
    req.POST.__setitem__('comment', comment)
    
    #return post_comment(req) 
    return comment_posted(request)
  else:
    data = request.POST.copy()
    object_pk = data.get("object_pk")
    if object_pk is None:
      #Ideally this should be replaced
      return HttpResponseNotFound("<h1>There was an error with your comment, please try again</h1>")
    try:
      target = Post.objects.get(pk=object_pk)
    except (ObjectDoesNotExist, ValueError, ValidationError):
      return HttpResponseNotFound("<h1>There was an error with your comment, please try again</h1>")

    form = ExtendedCommentForm(target, data=data)
    print "\n\nform incoming!!\n\n\n"
    print form
    if form.security_errors():
      return HttpResponseNotFound("<h1>There was an error with your comment, please try again</h1>")
    if form.is_valid():
      print "valid"
      form.save()
    #return post_comment(request)
    return comment_posted(request)

@require_POST
def post(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/')
  else:
    data = request.POST.copy()
    object_pk = data.get("object_pk")
    if object_pk is None:
      #Ideally this should be replaced
      return HttpResponseNotFound("<h1>There was an error with your comment, please try again</h1>")
    try:
      target = Post.objects.get(pk=object_pk)
    except (ObjectDoesNotExist, ValueError, ValidationError):
      return HttpResponseNotFound("<h1>There was an error with your comment, please try again</h1>")

    preview = "preview" in data
    
    if request.FILES:
      form = ExtendedCommentForm(target, request.FILES, data=data)
      if form.is_valid():
        handle_uploaded_file(request.FILES['file'])
    else:
      form = ExtendedCommentForm(target, data=data)
    print "\n\nform incoming!!\n\n\n"
    print form
    if form.security_errors():
      return HttpResponseNotFound("<h1>There was an error with your comment, please try again</h1>")
    if form.is_valid():
      print "valid"
      form.save()
    return comment_posted(request)


def handle_uploaded_file(f):
  path = os.path.join(MEDIA_ROOT, 'uploads/') + f.name
  destination = open(path, 'wb+')
  for chunk in f.chunks():
    destination.write(chunk)
  destination.close()

def comment_posted(request):
  if request.GET.__contains__('c'):
    comment_id = request.GET['c']
    comment = ExtendedComment.objects.get(pk=comment_id)

    if comment:
      return HttpResponseRedirect(comment.get_absolute_url())

  return HttpResponseRedirect("/")
