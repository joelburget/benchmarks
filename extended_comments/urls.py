from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^post/$', 'benchmarks.extended_comments.views.post'),
  (r'^posted/$', 'benchmarks.extended_comments.views.comment_posted'),
  #(r'^', include('django.contrib.comments.urls')),
)
