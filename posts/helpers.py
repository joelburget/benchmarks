import os
import commands
from benchmarks.settings import MEDIA_ROOT

INVALID_FILES = (
  r'^**$',
  r'^**$',
)

def handle_uploaded_file(f, postid):
  # Get folder name and create it
  path = os.path.join(MEDIA_ROOT, 'uploads/')
  path = os.path.join(path, str(postid) + '/')
  
  if not os.path.isdir(path):
    os.mkdir(path)

  # Write file
  path += f.name
  destination = open(path, 'wb+')

  for chunk in f.chunks():
    destination.write(chunk)
  destination.close()

  # Validate file
  validate(path)

def validate(path):
  # Get filetype
  #filetype = commands.getoutput('file ' % (path,))

  # Remove executable flag if needed
  #if filetype:
  #  os.system('chmod a-x ' % (path,))
  pass
