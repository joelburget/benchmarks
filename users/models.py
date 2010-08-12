from django import forms
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.forms import ModelForm

# Assign users to groups by default, makes code 100% bulletproof
def join_groups_on_create(sender, instance, created, **kwargs):
  # Check to see if we have a generic Users group
  g = Group.objects.get(name='Users')
  if not g:
   g = Group(name='Users')
   g.save()

  # Check to ensure we're making a new record, not updating one
  if created:
      instance.groups = [g]
      instance.save()
  else:
    # Updating record, check to see if user has left all groups
    if instance.groups.all() == []:
      # Ensure users are always at least a part of one group
      instance.groups = [g]
      instance.save()
      
post_save.connect(join_groups_on_create, sender=User)

# User Profiles
class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  bio = models.CharField(max_length=500)
  showemail = models.BooleanField(default=True)

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

  def group(self):
    """Returns the primary group of a user."""
    return self.user.groups.all()[0]

  def __unicode__(self):
    return 'Profile for %s' % (self.user.username,)

# Set up profiles for new users
def new_profile(sender, instance, created, **kwargs):
  if created:
    profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(new_profile, sender=User)

# Form for user objects
class UserForm(ModelForm):
  class Meta():
    model = User
    fields = ('first_name', 'last_name', 'email')

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required', 'size':'30'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required', 'size':'30'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'required email'}))
