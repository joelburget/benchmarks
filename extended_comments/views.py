from benchmarks.extended_comments.models import ExtendedComment
from benchmarks.extended_comments.forms import ExtendedCommentForm
from benchmarks.posts.models import Post
from benchmarks.settings import MEDIA_ROOT
import html5lib
from html5lib import sanitizer
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
    return render_to_response('comments/error.html', {'msg' :'There was an problem with your comment.'}, context_instance=RequestContext(request))
  try:
    target = Post.objects.get(pk=object_pk)
  except (ObjectDoesNotExist, ValueError, ValidationError):
    return render_to_response('comments/error.html', {'msg' :'There was an problem with your comment.'}, context_instance=RequestContext(request))

  preview = "preview" in data
  data.user = request.user
  
  form = ExtendedCommentForm(target, data=data)
  if request.FILES:
    if (form.is_valid() and not preview):
      handle_uploaded_file(request.FILES['file'])
  if form.security_errors():
    return render_to_response('comments/error.html', {'msg' :'There was an problem with your comment.'}, context_instance=RequestContext(request))
  if form.is_valid():
    comment = ExtendedComment(content_type = ContentType.objects.get(app_label='posts', model='post'),
                              object_pk = object_pk,
                              site_id = settings.SITE_ID,
                              user = request.user,
                              comment = form.cleaned_data["comment"],
                              published = datetime.datetime.now())
    if preview:
      comment = request.POST.__getitem__('comment')
      p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
      comment = p.parse(comment).childNodes[0].childNodes[1].toxml()[6:-7]
      
      return render_to_response(
          'comments/preview.html', {
            'comment': comment,#form.data.get('comment', ''),
            'form'   : form,
            },
          RequestContext(request)
      )

    else:
      comment.save()
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
  if request.GET.__contains__('c'):
    comment_id = request.GET['c']
    comment = ExtendedComment.objects.get(pk=comment_id)

    if comment:
      return HttpResponseRedirect(comment.get_absolute_url())

  return HttpResponseRedirect("/")
