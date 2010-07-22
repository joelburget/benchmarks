import os
import shutil
from django.utils.html import linebreaks
from benchmarks.settings import SITE_ROOT
from django.db.models.signals import pre_delete, pre_save
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from benchmarks.posts.widgets import MultiFileInput
from os.path import basename
from django import forms

# Post
CATEGORY_CHOICES = (
  ('P', 'Problem'),
  ('R', 'Realization'),
  ('V', 'Verification'),
  ('O', 'Other'),
)

class Post(models.Model):
  title = models.CharField(max_length=200)
  published = models.DateTimeField('Date Published', auto_now_add=True)
  body = models.TextField()
  sticky = models.BooleanField('Show on Frontpage?', default=False)
  author = models.ForeignKey(User)
  category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
  parent = models.ForeignKey('self', null=True, blank=True)

  def __unicode__(self):
    return self.title

  def get_absolute_url(self):
    return '/posts/%s/' % (self.pk,)

  def get_absolute_url_with_comments(self):
    return '%s#comments' % (self.get_absolute_url(),)

def newlines_to_brs(sender, instance, **kwargs):
  print instance.body
  instance.body = linebreaks(instance.body)

pre_save.connect(newlines_to_brs, sender=Post)

def clean_up_after_post(sender, instance, **kwargs):
  # Delete all postfiles
  for postfile in instance.postfile_set.all():
    postfile.delete()

  # Delete all comments

  # Clean up uploads directory
  path = os.path.join(SITE_ROOT, 'assets/uploads/%s/' % (instance.pk,))
  shutil.rmtree(path)

pre_delete.connect(clean_up_after_post, sender=Post)

# PostForm
class PostForm(ModelForm):
  title = forms.CharField(widget=forms.TextInput(attrs = {'class' : 'validate[required]'}))
  body = forms.CharField(widget=forms.TextInput(attrs = {'class' : 'validate[required]'}))

  class Meta():
    model = Post
    fields = ('title', 'body', 'category', 'parent')

# PostFile
def get_upload_path(instance, filename):
  return 'uploads/%s/%s' % (instance.post.pk, filename,)

class PostFile(models.Model):
  file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
  post = models.ForeignKey(Post)

  def __unicode__(self):
    return basename('%s' % (self.file,))
