import re
from django.conf import settings

class LastPage:
  def process_request(self, request):
    path = request.get_full_path()

    # Check for requests we don't want to check
    match = False
    for url in settings.LASTPAGE_SKIP:
      match = match or re.search(url, path)

    if not match:
      # Save last visited page
      if 'currentpage' in request.session:
        request.session['lastpage'] = request.session['currentpage']
    
      # Save current page
      request.session['currentpage'] = path
