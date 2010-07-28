# Thanks to http://tankadillo.com/custom-django-linebreaks-filter
import re
from django import template
from django.utils.functional import allow_lazy
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe, SafeData
from django.utils.encoding import force_unicode
from django.utils.html import escape
from html5lib import sanitizer

register = template.Library()

def pre_code_fix(s):
  return s

def linebreaks_smart_function_util(value, autoescape=False):
  BLOCK_ELEMENTS = sanitizer.HTMLSanitizerMixin.acceptable_elements
  value = re.sub(r'\r\n|\r|\n', '\n', force_unicode(value)) # normalize newlines
  paras = re.split('\n{2,}', value)
  parsedParas = []
  if autoescape:
   for p in paras:
    if re.match("<"+">|<".join(BLOCK_ELEMENTS) + ">", p, re.DOTALL):
      parsedParas.append(escape(p.strip()).replace('\n', '<br>'))
    else:
      parsedParas.append(u'<p>%s' % escape(p.strip()).replace('\n', '<br>'))
  else:
    for p in paras:
      if re.match("<"+">|<".join(BLOCK_ELEMENTS) + ">", p, re.DOTALL):
        parsedParas.append(p.replace('\n', '<br>'))
      else:
        parsedParas.append(u'<p>%s' % p.strip().replace('\n', '<br>'))
  return pre_code_fix(u'\n\n'.join(parsedParas))
linebreaks_smart_function = allow_lazy(linebreaks_smart_function_util, unicode)

@register.filter
def linebreaks_smart(value, autoescape=None):
  """
  Replaces line breaks in plain text with appropriate HTML; a single
  newline becomes an HTML line break (<br>) and a new line
  followed by a blank line becomes a paragraph break (<p>).
  Paragraphs beginning with an HTML block element (<div>) are not
  turned into HTML paragraphs.
  """
  autoescape = autoescape and not isinstance(value, SafeData)
  return mark_safe(linebreaks_smart_function(value, autoescape))
linebreaks_smart.is_safe = True
linebreaks_smart.needs_autoescape = True
linebreaks_smart = stringfilter(linebreaks_smart)
