import os
from benchmarks.settings import MEDIA_ROOT

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
  pass
