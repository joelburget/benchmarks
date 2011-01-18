from django.contrib.auth.models import User
from django import template

register = template.Library()

@register.simple_tag
def username(id):
  """
  Return the username corresponding to the user id
  """

  return User.objects.get(pk=id).username
