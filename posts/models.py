from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

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
  file = models.FileField(upload_to='uploads', null=True, blank=True)

  def __unicode__(self):
    return self.title

class PostForm(ModelForm):
  class Meta():
    model = Post
    fields = ('title', 'body', 'category', 'file')
