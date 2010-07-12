import os
import tarfile
import zipfile
import commands
from benchmarks.settings import MEDIA_ROOT
from benchmarks.posts.models import Post, PostFile

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

    filemod = PostFile(file=modelfile, post=post)
    filemod.save()
