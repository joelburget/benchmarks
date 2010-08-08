import commands
import os
import tarfile
import zipfile

from benchmarks.posts.models import Post, PostFile, PostForm
from benchmarks.settings import MEDIA_ROOT

def new_post(post, params):
  # Set content
  form = PostForm(params, instance = post)

  for e in form.errors:
    print ' error in modelform: %s' % (e,)
  
  if form.is_valid():
    # Data is ok
    form.save()
    return True
  else:
    # Data is invalid
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
      filemod = PostFile(file=modelfile, post=post)
      filemod.save()
