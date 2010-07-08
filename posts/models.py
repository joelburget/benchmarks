from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from benchmarks.posts.widgets import MultiFileInput

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

  def __unicode__(self):
    return self.title

  def get_absolute_url(self):
    return '/posts/%s/' % (self.pk,)

  def get_absolute_url_with_comments(self):
    return '%s#comments' % (self.get_absolute_url(),)

class PostForm(ModelForm):
  class Meta():
    model = Post
    fields = ('title', 'body', 'category')

class PostFile(models.Model):
  file = models.FileField(upload_to='uploads', null=True, blank=True)
  post = models.ForeignKey(Post)

  def __unicode__(self):
    return '%s' % (self.file,)
