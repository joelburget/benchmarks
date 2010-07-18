from django.conf.urls.defaults import *
from django.contrib.auth.models import User #do we need this?
from benchmarks.feeds import RssPersonalizedFeed, AtomPersonalizedFeed

urlpatterns = patterns('',
  # Note: Regex below is alphanumeric chars, and +, ., _, or -, min length 1, max 30
  # Follows Django username field requirements as specified in docs.
  (r'^(?P<uname>[a-zA-Z0-9_\@\+\.\-]{1,30})/$', 'benchmarks.users.views.showuser'),
  (r'^(?P<uname>[a-zA-Z0-9_\@\+\.\-]{1,30})/edit/$', 'benchmarks.users.views.edituser'),
  (r'^(?P<uname>[a-zA-Z0-9_\@\+\.\-]{1,30})/rss/$', RssPersonalizedFeed()),
  (r'^(?P<uname>[a-zA-Z0-9_\@\+\.\-]{1,30})/atom/$', AtomPersonalizedFeed()),
)
