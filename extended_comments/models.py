from django.db import models
from django.contrib.comments.models import BaseCommentAbstractModel
from django.contrib.auth.models import User
import datetime
from django.conf import settings

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

class ExtendedComment(BaseCommentAbstractModel):
  user = models.ForeignKey(User)
  published = models.DateTimeField('Date Published', auto_now_add=True)
  comment = models.TextField('comment', max_length=COMMENT_MAX_LENGTH)
  file = models.FileField(upload_to='uploads', null=True, blank=True)

  #I'm not sure if this class is really necessary, but the normal comment
  #model has it so better safe than sorry
  class Meta:
    ordering = ('published',)
    verbose_name = ('comment')
    verbose_name_plural = ('comments')

  def __unicode__(self):
    return "%s: %s..." % (self.user, self.comment[:50])

  #Again, not sure if this is necessary
  def save(self, *args, **kwargs):
    if self.published is None:
      self.published = datetime.datetime.now()
    super(ExtendedComment, self).save(*args, **kwargs)

  #In fact, I'm not sure about any of this
  def get_absolute_url(self, anchor_pattern="#c%(id)s"):
    return self.get_content_object_url() + (anchor_pattern % self.__dict__)

  def get_as_text(self):
    d = {
      'user': self.user,
      'date': self.published,
      'comment': self.comment,
      'domain': self.site.domain,
      'url': self.get_absolute_url()
    }
    return 'Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s' % d
