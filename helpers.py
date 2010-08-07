import os
from benchmarks.settings import SITE_ROOT

def generate_dirs_list(d):
  """Creates a list of <li> elements for usage in the AJAX file browser."""
  foldersresult = ''
  filesresult = ''
  files = os.listdir(d)

  # Loop through all files in this dir
  for f in files:
    # For output...
    oldf = f
    f = os.path.join(d, f)

    if os.path.isdir(f):
      # Directory
      relname = f.replace(SITE_ROOT, '') + '/'
      foldername = os.path.basename(f)
      foldersresult += '<li class="directory collapsed"><a href="#" rel="%s">%s</a></li>\n' % \
                       (relname, foldername,)
    else:
      # File
      relname = f.replace(SITE_ROOT + '/assets/', '')
      filename, fileext = os.path.splitext(f)
      fileext = fileext[1:]
      filename = os.path.basename(filename)
      filesresult += '<li class=" file ext_%s"><a href="#" rel="%s">%s</a></li>\n' % \
                     (fileext, relname, filename)

  # Return folders list w/files concatenated on
  return foldersresult + filesresult
