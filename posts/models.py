import markdown
from benchmarks.templatetags.templatetags.date_diff import date_diff

from django import forms
from django.contrib.auth.models import User, Group
from django.db.models import signals
from django.db import models

import os

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
  body_display = models.TextField(blank=True, null=True)
  author = models.ForeignKey(User)
  group = models.ForeignKey(Group)
  previous = models.ForeignKey('PostRevision', blank=True, null=True)
  published = models.DateTimeField(auto_now_add=True)
  category = models.CharField(max_length=1, choices=POSTTYPES)
  problem = models.ForeignKey('self', blank=True, null=True)
  files = models.ManyToManyField('PostFile', blank=True, null=True)
  up_to_date = models.BooleanField(default=True)

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
  body_display = models.TextField(blank=True, null=True)
  author = models.ForeignKey(User)
  group = models.ForeignKey(Group)
  previous = models.ForeignKey('PostRevision', blank=True, null=True)
  published = models.DateTimeField(auto_now_add=True)
  files = models.ManyToManyField('PostFile', blank=True, null=True)

  # Method
  def __unicode__(self):
    return str(date_diff(self.published))

def convert_markdown(sender, instance, **kwargs):
  instance.body_display = markdown.markdown(instance.body)

signals.pre_save.connect(convert_markdown, sender=Post)
signals.pre_save.connect(convert_markdown, sender=PostRevision)

#
# Files
#
FILETYPES = (
  ('S', 'Specs'),
  ('C', 'Code'),
  ('V', 'VCs'),
  ('O', 'Other'),
)

def get_upload_path(instance, filename):
  return 'uploads/posts/%s/%s' % (instance.pk, filename)

class PostFile(models.Model):
  file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
  filetype = models.CharField(max_length=1, choices=FILETYPES, default='O')

  def __unicode__(self):
    return os.path.basename(self.file.name)
