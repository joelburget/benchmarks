from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Example:
  # (r'^benchmarks/', include('benchmarks.foo.urls')),

  # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
  # to INSTALLED_APPS to enable admin documentation:
  # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # About/Getting started templates
  (r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
  (r'^getting-started/$', 'django.views.generic.simple.direct_to_template', {'template': 'getting-started.html'}),

  # Redirects
  (r'^admin/', include(admin.site.urls)),
  (r'^comments/', include('benchmarks.extended_comments.urls')),
  (r'^groups/', include('benchmarks.groups.urls')),
  (r'^posts/', include('benchmarks.posts.urls')),
  (r'^user/', include('benchmarks.users.urls')),

  # Login/logout
  (r'^login/$', 'benchmarks.posts.views.loginuser'),
  (r'^logout/$', 'benchmarks.posts.views.logoutuser'),

  # Root
  (r'^$', 'benchmarks.views.homepage'),
)

if settings.DEBUG:
  urlpatterns += patterns('django.views.static',
      (r'^static_media/(?P<path>.*)$', 'serve',
        {'document_root': settings.MEDIA_ROOT,
         'show_indexes': True}),)
