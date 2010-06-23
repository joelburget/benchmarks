from benchmarks.posts.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
  # Order by newest on top
  ordering = ('-published', )

  # Display multiple fields in the list view
  list_display = ('title', 'body', 'sticky')
  list_editable = ['sticky']

  # Filter and search capabilites
  list_filter = ['published']
  search_fields = ['title']

admin.site.register(Post, PostAdmin)
