from django.db import models
from django.contrib.comments.models import Comment
from django import forms

class ExtendedComment(Comment):
  pass

class UploadFileForm(forms.Form):
  file = forms.FileField()
