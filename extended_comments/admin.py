from benchmarks.extended_comments.models import ExtendedComment
from django.contrib import admin

class ExtendedCommentAdmin(admin.ModelAdmin):
  pass

admin.site.register(ExtendedComment, ExtendedCommentAdmin)
