import re
import urllib

from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

def __replace(m):
  CHARTS_URL = 'http://chart.apis.google.com/chart?cht=tx&chl='
  #return '<img src="%s" alt="%s" />' % (CHARTS_URL + urllib.quote_plus(m.group(1)), m.group(1))
  return '<img src="%s" alt="%s" />' % (CHARTS_URL + urllib.quote(m.group(1)), m.group(1))

@register.filter
@stringfilter
def tex_to_images(value):
  """Filter to replace a formula with a TeX image

  Usage:
  {{ "$$x^2$$"|tex_to_images }}

  Note:
  The image is downloaded from Google's Chart API.
  See http://code.google.com/apis/chart/docs/gallery/formulas.html

  """

  svalue = re.sub(
            '\$\$([^$]*)\$\$',
            __replace,
            value,
            re.DOTALL
  )

  return mark_safe(u'' + svalue)
tex_to_images.needs_autoescape = False
