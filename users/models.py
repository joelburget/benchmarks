from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  bio = models.CharField(max_length=200)

  def __unicode__(self):
    return 'Profile for %s' % (self.user.username,)

def new_profile(sender, instance, created, **kwargs):
  if created:
    profile, created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(new_profile, sender=User)

class UserForm(ModelForm):
  class Meta():
    model = User
    fields = ('first_name', 'last_name', 'email')

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required', 'size':'30'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required', 'size':'30'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'required email'}))
