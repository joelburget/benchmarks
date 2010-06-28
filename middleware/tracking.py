from django.conf import settings

class LastPage:
  def process_request(self, request):
    path = request.get_full_path()

    # Check for requests we don't want to check
    if not (path.find(settings.MEDIA_URL) == 0 or path == '/favicon.ico'):

      # Save last visited page
      if 'currentpage' in request.session:
        request.session['lastpage'] = request.session['currentpage']
    
      # Save current page
      request.session['currentpage'] = path
