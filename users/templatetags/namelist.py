from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def namelist(users):
  l = [user.username for user in users]

  s = ''
  for u in l:
    s += u + ' '
  return s[:-1]
