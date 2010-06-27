from django.conf.urls.defaults import *
from django.contrib.auth.models import Group

urlpatterns = patterns('',
  (r'^$', 'benchmarks.groups.views.index'),
  (r'^(?P<group_id>\d+)$', 'benchmarks.groups.views.detail'),
)
