from django.conf.urls.defaults import *
from benchmarks.posts.models import Post
from django.views.generic.list_detail import object_detail

info_dict = {
  'queryset': Post.objects.all(),
}

urlpatterns = patterns('',
  (r'^(?P<object_id>\d+)/$', 'object_detail', info_dict),
)
