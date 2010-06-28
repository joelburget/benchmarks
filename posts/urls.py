from django.conf.urls.defaults import *
from benchmarks.posts.models import Post

info_dict = {
  'queryset': Post.objects.all(),
}

urlpatterns = patterns('',
  # View posts
  (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', dict(info_dict)),

  # Login/logout
  (r'^login/$', 'benchmarks.posts.views.loginuser'),
  (r'^logout/$', 'benchmarks.posts.views.logoutuser'),
)
