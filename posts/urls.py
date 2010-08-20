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
  (r'^categorize/$', 'benchmarks.posts.views.categorize'),
  (r'^(?P<post_id>\d+)/edit/$', 'benchmarks.posts.views.editpost'),

  # AJAX post history
  (r'^(?P<post_id>\d+)/history/(?P<post_history_id>.+)/info/$', 'benchmarks.posts.views.revision_info'),
  (r'^(?P<post_id>\d+)/history/(?P<post_history_id>.+)/$', 'benchmarks.posts.views.posthistory'),
)
