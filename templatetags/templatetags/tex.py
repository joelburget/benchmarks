import re
import hashlib

from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

from benchmarks.templatetags.helpers.latexmath2png import math2png
from benchmarks.settings import MEDIA_ROOT, MEDIA_URL

register = template.Library()

@register.filter
@stringfilter
def tex_to_images(value):
  """Filter to replace a formula with a TeX image

  Usage:
  {{ "$$x^2$$"|tex_to_images }}

  Note:
  The image is created on the server and stored in the
  {{ MEDIA_URL }}formulas/ directory. The server must
  have a working installation of LaTeX and dvipng.

  """

  def __replace(m):
    formula = m.group(1)

    # hash the formula to make a unique url
    h = hashlib.sha1()
    h.update(formula)

    # use hexdigest because digest produces possibly unsafe characters 
    hash = h.hexdigest() 

    # create and save image
    dir = MEDIA_ROOT + "/formulas/"
    math2png([formula], dir, prefix=hash)
                         
    return '<img src="%sformulas/%s1.png" alt="%s" />' \
        % (MEDIA_URL, hash, formula)

  # note on the regex: because of the '?', it matches
  # in a minimal way, so every formula will be matched
  # separately
  svalue = re.sub(
            '\$\$(.*?)\$\$',
            __replace,
            value,
            re.DOTALL
  )

  return mark_safe(u'' + svalue)
tex_to_images.needs_autoescape = False
