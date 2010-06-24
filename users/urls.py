from django.conf.urls.defaults import *
from django.contrib.auth.models import User

urlpatterns = patterns('',
  # Note: Regex below is alphanumeric chars, and +, ., _, or -, min length 1, max 30
  # Follows Django username field requirements as specified in docs.
  (r'^(?P<uname>[a-zA-Z0-9_\@\+\.\-]{1,30})/$', 'benchmarks.users.views.showuser'),
)
