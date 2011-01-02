from benchmarks.posts.models import *
from benchmarks.reversion.helpers import patch_admin
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
  # Order by newest on top
  ordering = ('-published', )

  # Display multiple fields in the list view
  list_display = ('title', 'body')

  # Filter and search capabilites
  list_filter = ['published']
  search_fields = ['title']

admin.site.register(Post, PostAdmin)
admin.site.register(PostFile)
patch_admin(Post)
