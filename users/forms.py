from django import forms
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User

# Form for user objects
class UserForm(ModelForm):
  class Meta():
    model = User
    fields = ('first_name', 'last_name', 'email')

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required', 'size':'30'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'required', 'size':'30'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'required email'}))
