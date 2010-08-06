from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.models import Group

# Enable Admin
from django.contrib import admin
admin.autodiscover()

# Enable Custom 404
handler404 = 'benchmarks.views.our404'
handler500 = 'benchmarks.views.our500'

urlpatterns = patterns('',
  # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
  # to INSTALLED_APPS to enable admin documentation:
  # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # About/Getting started/Sanitizing templates
  (r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
  (r'^getting-started/$', 'django.views.generic.simple.direct_to_template', {'template': 'getting-started.html'}),
  (r'^sanitizing/$', 'django.views.generic.simple.direct_to_template', {'template' : 'sanitizing.html'}),

  # App Redirects
  (r'^admin/', include(admin.site.urls)),
  (r'^comments/', include('benchmarks.extended_comments.urls')),
  (r'^groups/', include('benchmarks.groups.urls')),
  (r'^posts/', include('benchmarks.posts.urls')),
  (r'^users/', include('benchmarks.users.urls')),

  # Feeds
  (r'^rss/$', 'benchmarks.views.rss'),
  (r'^atom/$', 'benchmarks.views.atom'),

  # Login/logout
  (r'^login/$', 'benchmarks.views.loginuser'),
  (r'^logout/$', 'benchmarks.views.logoutuser'),

  # Join
  (r'^join/$', 'django.views.generic.simple.direct_to_template', {'template':'users/join.html', 'extra_context' : {'grouplist' : Group.objects.all() }}),
  (r'^joined/$', 'benchmarks.views.joined'),

  # AJAX/API actions
  (r'^dirlist.*$', 'benchmarks.views.dirlist'),

  # Root
  (r'^$', 'benchmarks.views.homepage'),
)

if settings.DEBUG:
  urlpatterns += patterns('django.views.static',
      (r'^static_media/(?P<path>.*)$', 'serve',
        {'document_root': settings.MEDIA_ROOT,
         'show_indexes': True}),)
