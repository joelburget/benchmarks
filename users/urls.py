from django.conf.urls.defaults import *
from django.contrib.auth.models import User

urlpatterns = patterns('',
  (r'^(?P<uname>[a-zA-Z0-9_]{3,16})/$', 'benchmarks.users.views.showuser'),
)
