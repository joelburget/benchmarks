import os
import zipfile
import commands
from benchmarks.settings import MEDIA_ROOT
from benchmarks.posts.models import Post, PostFile

def validate_file(file):
  return True

def unzip_file(filepath, post):
  # Get zipfile and paths
  z = zipfile.ZipFile(filepath, 'r')
  outputpath = os.path.split(filepath)[0]

  # Extract
  z.extractall(path=outputpath)

  # Add all files to the post
  for name in z.namelist():
    unzippedfile = os.path.join(outputpath, name)
    modelfile = 'uploads/%s/%s' % (post.pk, name,) 

    filemod = PostFile(file=modelfile, post=post)
    filemod.save()
