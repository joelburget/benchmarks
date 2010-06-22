from django.conf.urls.defaults import *
from benchmarks.posts.models import Post

info_dict = {
  'queryset': Post.objects.all(),
}

urlpatterns = patterns('',
  (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
)
