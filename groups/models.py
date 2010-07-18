from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import Group

class GroupProfile(models.Model):
  group = models.OneToOneField(Group)
  about = models.CharField(max_length=500)
  link = models.URLField()

def new_profile(sender, instance, created, **kwargs):
  if created:
    profile, created = GroupProfile.objects.get_or_create(group=instance)

post_save.connect(new_profile, sender=Group)
