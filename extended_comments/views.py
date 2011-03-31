import datetime
import os

from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.http import require_POST
from django.http import HttpResponseNotFound
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from benchmarks.helpers import get_page_of_objects
from benchmarks.extended_comments.models import ExtendedComment, ExtendedCommentFile
from benchmarks.extended_comments.forms import ExtendedCommentForm
from benchmarks.extended_comments.decompress import decompress
from benchmarks.posts.models import Post
from django.db.models import Q
from django.contrib.auth.models import User
from benchmarks.settings import MEDIA_ROOT, SITE_ROOT
from benchmarks.helpers import redirect_to_error

#This sanitizes the input the user will see in the preview area for comments
#because that is not covered by the sanitization in comment-sanitizer/__init__.py
#(We want them to see what will actually show up)
@require_POST
@login_required
def post(request):
  data = request.POST.copy()
  if not data.get('name', ''):
    data['name'] = request.user.get_full_name() or request.user.username
  if not data.get('email', ''):
    data['email'] = request.user.email

  object_pk = data.get("object_pk")
  if object_pk is None:
    return redirect_to_error(403, "There was a problem with your comment.")
    #return render_to_response('comments/error.html', {'msg' :'There was an problem with your comment.'}, context_instance=RequestContext(request))
  try:
    target = Post.objects.get(pk=object_pk)
  except (ObjectDoesNotExist, ValueError, ValidationError):
    return redirect_to_error(403, "There was a problem with your comment.")
    #return render_to_response('comments/error.html', {'msg' :'There was an problem with your comment.'}, context_instance=RequestContext(request))

  preview = "preview" in data
  data.user = request.user
  
  form = ExtendedCommentForm(target, data=data)
  if form.security_errors():
    #return render_to_response('comments/error.html', {'msg' :'There was an problem with your comment.'}, context_instance=RequestContext(request))
    return redirect_to_error(403, "There was a problem with your comment.")
  if form.is_valid():
    comment = ExtendedComment(content_type = ContentType.objects.get(app_label='posts', model='post'),
                              object_pk = object_pk,
                              site_id = settings.SITE_ID,
                              user = request.user,
                              comment = form.cleaned_data["comment"],
                              published = datetime.datetime.now())
    if preview:
      comment = request.POST.__getitem__('comment')
      
      return render_to_response(
          'comments/preview.html', {
            'comment': comment,#form.data.get('comment', ''),
            'form'   : form,
            },
          RequestContext(request)
      )

    else:
      comment.save()

      if request.FILES:
        thisFile = request.FILES['file']
        #This is obviously horrible. I would love for it to be written as:
        #cf = ExtendedCommentFile(file=thisFile, parent=comment)
        #cf.save()
        #
        #However, the comment doesn't have a pk yet so ever comment ends up
        #being saved to the same folder, 'None.'
        #Please fix!
        cf = ExtendedCommentFile()
        cf.parent = comment
        cf.save()
        cf.file = thisFile
        cf.save()

        zippath = os.path.join(SITE_ROOT, 'assets/') + str(cf.file)
        decompress(zippath, comment)

  elif preview:
    return render_to_response(
      'comments/preview.html', {
        'comment': form.data.get('comment', ''),
        'form'   : form,
        },
      RequestContext(request)
    )
  else:
    return render_to_response('comments/error.html', {'msg' :'There was an problem with your comment.'}, context_instance=RequestContext(request))
  return comment_posted(request)

def handle_uploaded_file(f):
  path = os.path.join(MEDIA_ROOT, 'uploads/') + f.name
  destination = open(path, 'wb+')
  for chunk in f.chunks():
    destination.write(chunk)
  destination.close()

def comment_posted(request):
  # Redirect to the bottom of the comments section
  id = request.POST.get('object_pk', None)
  post = Post.objects.get(pk=id)

  if post:
    return HttpResponseRedirect("%s#leaveAComment" % \
      (post.get_absolute_url(),))
  else:
    return redirect_to_error(403, "/")

# This method is almost exactly the same as the one in posts/views.py. It might
# be worth it to factor out the duplicate functionality. Probably not.
def index(request):
  userlist = User.objects.all()

  if not 'searchtxt' in request.GET:
    # No searching, just render a paginated view of all posts
    comments = get_page_of_objects(ExtendedComment.objects.all() \
                                .order_by('-published'), request)
    return render_to_response('comments/index.html', \
                              { 'comments':comments, 'userlist' : userlist }, \
                              context_instance=RequestContext(request))
  else:
    # Search performed
    searchtxt = request.GET['searchtxt']  # main search textbox
    user = request.GET.get('user', '')    # advanced - author

    if user == '':
      # Ugly hack
      userq = ~Q(pk=0)
    else:
      u = userlist.filter(username=user)
      userq = Q(user=u)

    # Advanced query
    pcomments = ExtendedComment.objects.filter(
      Q(comment__icontains=searchtxt),
      userq
    ).distinct().order_by('-published')

    # Render
    comments = get_page_of_objects(pcomments, request)
    return render_to_response('comments/index.html', {
      'searchtxt' : searchtxt,
      'u' : user,
      'userlist' : userlist,
      'comments' : comments,
    },
    context_instance=RequestContext(request))
