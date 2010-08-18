import os
import shutil
from datetime import datetime
from os.path import basename

from benchmarks.settings import SITE_ROOT
from benchmarks.templatetags.templatetags.date_diff import date_diff

from django import forms
from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_delete, pre_save
from django.db import models
from django.forms import ModelForm

#
# Post types
#
class Post(models.Model):
  # Attributes
  title = models.CharField(max_length=200)
  body = models.TextField()
  author = models.ForeignKey(User)
  group = models.ForeignKey(Group)
  previous = models.ForeignKey('PostRevision', blank=True, null=True)
  published = models.DateTimeField(auto_now_add=True)

  # Methods
  def __unicode__(self):
    return '%s (%s, %s)' % (self.title, self.author, self.group)

  def get_absolute_url(self):
    return '/posts/%s' % (self.pk,)

  def get_comments_absolute_url(self):
    return '%s#comments' % (self.get_permalink(),)

  def save_revision(self, data):
    pass

  def get_revisions(self):
    if self.previous == None:
      return [self]

    hist = []
    cur = self

    while cur.previous != None:
      cur = cur.previous
      hist.append(cur)

    return hist

class Problem(Post):
  pass

class Solution(Post):
  problem = models.ForeignKey(Problem)

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
    return 'Revision %s (%s, %s)' % (self.published, self.author, self.group)

#
# Files
#
class PostFile(models.Model):
  pass

#
# Forms
#
class PostForm(ModelForm):
  title = forms.CharField(widget=forms.TextInput(attrs = {'class' : 'validate[required]'}))
  body = forms.CharField(widget=forms.widgets.Textarea())

  class Meta():
    model = Post
    fields = ('title', 'body', 'parent')

class ProblemForm(PostForm):
  class Meta():
    model = Problem

class SolutionForm(PostForm):
  class Meta():
    model = Solution
