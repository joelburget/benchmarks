import os
from benchmarks.settings import SITE_ROOT

def generate_dirs_list(d):
  foldersresult = ''
  filesresult = ''
  files = os.listdir(d)

  for f in files:
    oldf = f
    f = os.path.join(d, f)

    if os.path.isdir(f):
      relname = f.replace(SITE_ROOT, '') + '/'
      foldername = os.path.basename(f)
      foldersresult += '<li class="directory collapsed"><a href="#" rel="%s">%s</a></li>\n' % (relname, foldername,)
    else:
      relname = f.replace(SITE_ROOT + '/assets/', '')
      filename, fileext = os.path.splitext(f)
      fileext = fileext[1:]
      filename = os.path.basename(filename)
      filesresult += '<li class=" file ext_%s"><a href="#" rel="%s">%s</a></li>\n' % (fileext, relname, filename)

  return foldersresult + filesresult
