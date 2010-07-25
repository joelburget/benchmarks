import re
import urllib
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

def __replace(m):
  CHARTS_URL = 'http://chart.apis.google.com/chart?cht=tx&chl='
  return '<img src="%s" alt="%s" />' % (CHARTS_URL + urllib.quote_plus(m.group(1)), m.group(1))

@register.filter
@stringfilter
def tex_to_images(value):
  svalue = re.sub(
            '\$\$(.+)\$\$',
            __replace,
            value,
            re.DOTALL
  )

  return mark_safe(u'' + svalue)
tex_to_images.needs_autoescape = False
