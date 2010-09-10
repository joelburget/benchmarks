from benchmarks.users.models import UserProfile
from django import forms
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User

class UserForm(ModelForm):
  class Meta():
    model = User
    fields = ('first_name', 'last_name', 'email')

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required', 'size':'30'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required', 'size':'30'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'required email'}))

class UserProfileForm(ModelForm):
  class Meta():
    model = UserProfile
    fields = ('bio', 'showemail', 'commentResponseSubscribe', \
              'ownPostCommentSubscribe', 'groupPostSubscribe', \
              'allProblemSubscribe')

  def __init__(self, *args, **kwargs):
    super(ModelForm, self).__init__(*args, **kwargs)
    self.fields['bio'].label = 'Bio'
    self.fields['showemail'].label = 'Show email?'
    self.fields['commentResponseSubscribe'].label = 'Subscribe to comments in posts you have commented on?'
    self.fields['ownPostCommentSubscribe'].label = 'Subscribe to posts you have commented on?'
    self.fields['groupPostSubscribe'].label = 'Subscribe to posts by members of your group?'
    self.fields['allProblemSubscribe'].label = 'Subscribe to all problems?'
