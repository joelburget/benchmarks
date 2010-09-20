import markdown2
from benchmarks.templatetags.templatetags.date_diff import date_diff
from benchmarks.templatetags.helpers.latexmath2png import math2png
from benchmarks.settings import MEDIA_ROOT, MEDIA_URL

from django import forms
from django.contrib.auth.models import User, Group
from django.db.models import signals
from django.db import models

import os
from multiprocessing import Process, Queue
from Queue import Empty

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

  def render_equations(self):
    """Fill in display_body and create equation images

    Note:
    The image is created on the server and stored in the
    {{ MEDIA_URL }}formulas/ directory. The server must
    have a working installation of LaTeX and dvipng.
    
    """

    #
    # Helpers
    #

    # This is always spawned as a separate process
    def make_images(q):
      eq = None
      while True:
        try:
          (eq, hash) = q.get(timeout=1)
          # create and save image
          dir = MEDIA_ROOT + "/formulas/"
          math2png([eq], dir, prefix=hash)
        except Empty:
          return

    q = Queue()
    p = Process(target=make_images, args=(q,))
    p.start()
    
    def __replace(m):
      formula = m.group(1)

      # hash the formula to make a unique url
      h = hashlib.sha1()
      h.update(formula)

      # use hexdigest because digest produces possibly unsafe characters
      hash = h.hexdigest() 

      # This sends the formula to the other thread to render as an image
      q.put((formula, hash))
                           
      # Notice the extra 1 before ".png" that shows up in the hash for some
      # reason.
      return '<img src="%sformulas/%s1.png" alt="%s" />' \
          % (MEDIA_URL, hash, formula)

    #
    # Endhelpers
    #

    svalue = re.sub(
        '\$\$(.*?)\$\$',
        __replace,
        self.display_body,
        re.DOTALL)

    # If you're brave, remove the following line, and the user will get their
    # response without having to wait for the images to render. Probably.
    p.join()

    self.display_body = svalue
    self.save()

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
  instance.body_display = markdown2.markdown(instance.body)

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
