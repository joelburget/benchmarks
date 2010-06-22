from django.db import models

#we can add more later
#we may want a user and a group model
#not sure if we can use what django provides us...

class Post(models.Model):
  title = models.CharField(max_length=200)
  slug = models.SlugField('Slug')
  published = models.DateTimeField('Date Published', auto_now_add=True)
  body = models.TextField()

  def __unicode__(self):
    return self.title
