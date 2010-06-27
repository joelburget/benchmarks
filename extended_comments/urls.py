from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^post/$', 'benchmarks.extended_comments.views.post'),
  (r'^', include('django.contrib.comments.urls')),
)
