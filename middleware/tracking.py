import re
from django.conf import settings

class LastPage:
  # Tuple of regular expressions
  # The LastPage middleware will skip tracking these.
  __skip = (
    r'^/dirlist.*$',
    r'^/favicon.ico$',
    r'^/' + settings.MEDIA_URL + '.*$',
  )

  def process_request(self, request):
    path = request.get_full_path()

    # Check for requests we don't want to check
    match = False

    for url in self.__skip:
      match = match or re.search(url, path)

    if not match:
      # Save last visited page
      if 'currentpage' in request.session:
        request.session['lastpage'] = request.session['currentpage']
    
      # Save current page
      request.session['currentpage'] = path
