from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from benchmarks.posts.widgets import MultiFileInput

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
  parent = models.ForeignKey('self', null=True)

  def __unicode__(self):
    return self.title

  def get_absolute_url(self):
    return '/posts/%s/' % (self.pk,)

  def get_absolute_url_with_comments(self):
    return '%s#comments' % (self.get_absolute_url(),)

# PostForm
class PostForm(ModelForm):
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
    return '%s' % (self.file,)
