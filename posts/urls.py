from django.conf.urls.defaults import *
from benchmarks.posts.models import Post
from benchmarks.settings import SITE_ROOT

urlpatterns = patterns('',
  # Index
  (r'^$', 'benchmarks.posts.views.index'),

  # View posts
  (r'^(?P<object_id>\d+)/$', 'benchmarks.posts.views.detail'),

  # Edit post
  (r'^new/$', 'benchmarks.posts.views.new'),
  (r'^(?P<post_id>\d+)/upload/$', 'benchmarks.posts.views.upload'),
  (r'^(?P<post_id>\d+)/manage/$', 'benchmarks.posts.views.manage'),
  (r'^(?P<post_id>\d+)/description/$', 'benchmarks.posts.views.description'),

  # AJAX post history
  (r'^(?P<post_id>\d+)/history/(?P<post_history_id>[a-zA-Z0-9]+)(/.+)*/$', 'benchmarks.posts.views.posthistory'),
  (r'^(?P<post_id>\d+)/files/(?P<post_history_id>[a-zA-Z0-9]+)(/.+)*/$', 'benchmarks.posts.views.postfiles'),
)
