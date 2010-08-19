from django import forms
from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_delete, pre_save
from django.db import models
from django.forms import ModelForm

from benchmarks.templatetags.templatetags.date_diff import date_diff

#
# Post types
#
POSTTYPES = (
  ('P', 'Problem'),
  ('S', 'Solution'),
)

class Post(models.Model):
  # Attributes
  title = models.CharField(max_length=200)
  body = models.TextField()
  author = models.ForeignKey(User)
  group = models.ForeignKey(Group)
  previous = models.ForeignKey('PostRevision', blank=True, null=True)
  published = models.DateTimeField(auto_now_add=True)
  category = models.CharField(max_length=1, choices=POSTTYPES)
  problem = models.ForeignKey('self', blank=True, null=True)

  # Methods
  def __unicode__(self):
    return str(date_diff(self.published))

  def get_absolute_url(self):
    return '/posts/%s/' % (self.pk,)

  def get_comments_absolute_url(self):
    return '%s#comments' % (self.get_permalink(),)

  def save_revision(self, data):
    pass

  def get_revisions(self):
    hist = [self]

    if self.previous == None:
      return hist

    cur = self
    while cur.previous != None:
      cur = cur.previous
      hist.append(cur)

    return hist

#
# Revisions
#
class PostRevision(models.Model):
  # Attributes
  body = models.TextField()
  author = models.ForeignKey(User)
  group = models.ForeignKey(Group)
  previous = models.ForeignKey('PostRevision', blank=True, null=True)
  published = models.DateTimeField(auto_now_add=True)

  # Method
  def __unicode__(self):
    return str(date_diff(self.published))

#
# Files
#
FILETYPES = (
  ('S', 'SPECS'),
  ('C', 'CODE'),
  ('V', 'VCS'),
  ('O', 'OTHER'),
)

def get_upload_path(instance, filename):
  return '%s/%s' % (instance.postrevision_set.all()[0].pk, filename)

class PostFile(models.Model):
  file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
  filetype = models.CharField(max_length=1, choices=FILETYPES)
  post_revision = models.ForeignKey(PostRevision, null=True)

#
# Forms
#
class PostForm(ModelForm):
  class Meta():
    model = Post
