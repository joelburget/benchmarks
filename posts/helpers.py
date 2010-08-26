import os
import tarfile
import zipfile

from benchmarks.posts.models import PostFile, PostForm, PostRevision

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
