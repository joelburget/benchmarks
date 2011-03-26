from benchmarks.settings import MEDIA_URL
from django import template
from posts.models import PostFile
from reversion.models import Version

register = template.Library()

@register.simple_tag
def version(file, rev):
  num_files = Version.objects.get_for_object(file).count()

  if num_files >= rev:
    return '<li class="%s-file"><a href="%s%s">%s</a> - %s' % (file.filetype, MEDIA_URL, file.file, file, file.get_filetype_display())
  else:
    return ""
