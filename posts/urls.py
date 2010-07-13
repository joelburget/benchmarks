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
  # NOTE: Just using posts here, because / redirects to post urls
  # Not ideally in the right location, but it works
  (r'^$', 'django.views.generic.list_detail.object_list', dict(info_dict)),

  # View posts
  (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', dict(info_dict)),

  # Edit post
  (r'^new/$', 'benchmarks.posts.views.editpost'),

  # Search posts
  (r'^search/$', 'benchmarks.posts.views.search'),
)
