from django.db import models
from django import forms
from django.contrib.auth.models import User

class Post(models.Model):
  title = models.CharField(max_length=200)
  published = models.DateTimeField('Date Published', auto_now_add=True)
  body = models.TextField()
  sticky = models.BooleanField('Show on Frontpage?', default=False)
  author = models.ForeignKey(User)

  def __unicode__(self):
    return self.title

class UploadFileForm(forms.Form):
  file  = forms.FileField()
