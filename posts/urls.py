from django.conf.urls.defaults import *
from benchmarks.posts.models import Post
from benchmarks.settings import SITE_ROOT

info_dict = {
  'queryset': Post.objects.all(),
  'extra_context' : {
    'SITE_ROOT' : SITE_ROOT,
  }  
}

urlpatterns = patterns('',
  # Index
  (r'^$', 'benchmarks.posts.views.index'),

  # View posts
  (r'^(?P<object_id>\d+)/$', 'benchmarks.posts.views.detail'),

  # Edit post
  (r'^new/$', 'benchmarks.posts.views.newpost'),
  (r'^(?P<post_id>\d+)/manage_files/$', 'benchmarks.posts.views.manage_files'),
  (r'^(?P<post_id>\d+)/edit/$', 'benchmarks.posts.views.editpost'),

  # Send users here after creating a new post
  (r'^(?P<post_id>\d+)/created/$', 'benchmarks.posts.views.created'),

  # AJAX post history
  (r'^(?P<post_id>\d+)/history/(?P<post_history_id>[a-zA-Z0-9]+)(/.+)*/$', 'benchmarks.posts.views.posthistory'),
)
