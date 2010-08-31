import os
import tarfile
import zipfile

from benchmarks import settings
from benchmarks.posts.models import PostFile, PostForm, PostRevision

from django.core.mail import EmailMessage

def new_post(post, params):
  # Set content
  form = PostForm(params, instance = post)

  if form.is_valid():
    # Data is ok
    form.save()
    return True
  else:
    # Data is invalid
    print form.errors
    return False

def update_post(post, params, user):
  if params.get('body', ''):
    # Move old content into a Revision
    rev = PostRevision(author = user)
    rev.body = post.body
    rev.group = post.group
    rev.save()

    # Fill post with new, edited data
    post.body = params['body']

    # Check for substantial edits
    if params.get('substantial', None) and post.category == 'P':
      for child in post.post_set.all(): 
        # Mark children as out of date
        child.up_to_date = False
        child.save()

        # Notify authors
        if settings.EMAIL_ENABLED and child.author.email != '':
          email = EmailMessage('OSU Benchmarks - "%s" Updated' % (post.title,),
                               'This message was automatically sent to you on '\
                               'behalf of the OSU Benchmarks application.\n\n'\
                               'The problem, "%s," has been updated, and this '\
                               'directly affects your solution, "%s."\n\n'\
                               'The change to the parent problem was marked '\
                               'substantial, meaning all accompanying '\
                               'solutions need to be updated to comply with '\
                               'the new specifications of the problem.'\
                                % (post.title, child.title),
                               to=[child.author.email])
          email.send()

    # If we're updating a post, it is up_to_date
    post.up_to_date = True

    # Link up histories
    if post.previous != None:
      # History already exists for this post
      last_revision = post.previous
      rev.previous = last_revision  # update chain
      post.previous = rev

      rev.save()
      post.save()
    else:
      # No history yet, only 1 new history object
      post.previous = rev
      post.save()

    return True
  else:
    # Invalid data, return false error code
    return False

def decompress(filepath, post):
  # Get output path
  outputpath = os.path.split(filepath)[0]

  if zipfile.is_zipfile(filepath):
    # Zipfiles
    z = zipfile.ZipFile(filepath, 'r')
    z.extractall(path=outputpath)
    files = z.namelist()
  elif tarfile.is_tarfile(filepath):
    # Tarballs
    t = tarfile.open(filepath)
    t.extractall(path=outputpath)
    files = t.getnames()
    t.close()
  else:
    # None, file list is empty, so we don't add to model
    files = []

  # Add all files to the post
  for name in files:
    unzippedfile = os.path.join(outputpath, name)
    modelfile = 'uploads/%s/%s' % (post.pk, name,) 

    # Note, don't add directories, otherwise Django can't remove them without
    # complaining with error messages.
    if not os.path.isdir(unzippedfile):
      #filemod = PostFile(file=modelfile, post=post)
      filemod = PostFile(file=modelfile)
      filemod.save()
      post.files.add(filemod)
      post.save()
