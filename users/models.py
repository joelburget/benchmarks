from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save

# User Profiles
class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  bio = models.TextField()
  showemail = models.BooleanField(default=True)
  group = models.ForeignKey(Group, null=True)

  # Personalized rss subscriptions
  # This may not be the right place to put these
  commentResponseSubscribe = models.BooleanField(default=True)
  ownPostCommentSubscribe = models.BooleanField(default=True)
  groupPostSubscribe = models.BooleanField(default=True)
  allProblemSubscribe = models.BooleanField(default=True)

  def get_display_name(self):
    if self.user.first_name:
      return self.user.first_name + ' ' + self.user.last_name
    else:
      return self.user.username

  def __unicode__(self):
    return 'Profile for %s' % (self.user.username,)

# Set up profiles for new users
def new_profile(sender, instance, created, **kwargs):
  if created:
    profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(new_profile, sender=User)
