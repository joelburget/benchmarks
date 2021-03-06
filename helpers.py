import os
from benchmarks.settings import SITE_ROOT, MEDIA_URL
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.loader import render_to_string
from django.http import HttpResponse

def redirect_to_error(status_code, msg):
  """Returns an error page for view functions to render

  Arguments:
  msg -- Text message to display
  status_code -- HTTP Status code to return

  Returns:
  A Response object of an error page

  """

  content = render_to_string('error.html', \
      { 'msg':msg, 'status_code':status_code, 'MEDIA_URL': MEDIA_URL })
  return HttpResponse(content, status=status_code)

def get_page_of_objects(objects, request):
  """Gets a given page of objects

  Arguments:
  objects -- List of objects to paginate
  request -- Request to parse for page number

  Returns:
  A response object of the page requested

  """

  # Get paginator for objects
  paginator = Paginator(objects, 10)
  
  # Get page
  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  # Grab page of objects
  try:
    objects = paginator.page(page)
  except (EmptyPage, InvalidPage):
    objects = paginator.page(paginator.num_pages)

  # Return page of objects
  return objects

def generate_dirs_list(d):
  """Creates a list of <li> elements for usage in the AJAX file browser.
  
  Arguments:
  d -- directory to start in

  Returns:
  An HTML list of the files and subdirectories in d
  
  """
  foldersresult = ''
  filesresult = ''
  files = os.listdir(d)

  # Loop through all files in this dir
  for f in files:
    # For output...
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
