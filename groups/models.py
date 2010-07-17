from django.db import models
from django.contrib.auth.models import Group

class GroupProfile(models.Model):
  group = models.ForeignKey(Group, unique=True)
  about = models.CharField(max_length=500)
