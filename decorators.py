from django.views.generic.simple import redirect_to
from django.http import HttpResponseForbidden

def require_ajax(function=None, redirect_url=None):
  """Decorator that makes sure the request is sent using ajax

  Keyword Arguments:
  function -- the function to decorate
  redirect_url -- The url to redirect to if the request is not ajax

  """
  def decorated(request, *args, **kwargs):
    if not request.is_ajax():
      if redirect_url:
        return redirect_to(redirect_url)
      else:
        return HttpResponseForbidden('This url only accepts ajax requests.')
    return function(request, *args, **kwargs)

  return decorated
