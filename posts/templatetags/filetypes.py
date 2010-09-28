from benchmarks.posts.models import FILETYPES
from benchmarks.settings import MEDIA_URL
from django import template

register = template.Library()

@register.simple_tag
def filetypes(post):
  out = ""

  # Get files, and count
  files = post.files.all()
  count = num = len(FILETYPES)

  # Loop through files
  for file in files:
    filetype = file.filetype

    # Loop through filetypes
    out += "<li>"
    count = 0

    for type in FILETYPES:
      abbr, name = type

      # Get class for pill buttons
      if count == 0:
        klass = "lpill"
      elif count == num - 1:
        klass = "rpill"
      else:
        klass = ""

      # Generate output
      checked = 'checked' if filetype == abbr else ''
      out += '<input type="radio" value="%s%s" name="%s" %s/>' % (file.pk, abbr, file.pk, checked)
      out += '<label for="%s%s" class="%s">%s</label>' % (file.pk, abbr, klass, name)

      # Next filetype
      count += 1

    out += '<a href="%s%s">%s</a></li>' % (MEDIA_URL, file.file, file.file.name)
      
  return out
