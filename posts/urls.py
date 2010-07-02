from django.conf.urls.defaults import *
from benchmarks.posts.models import Post

info_dict = {
  'queryset': Post.objects.all(),
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
)
