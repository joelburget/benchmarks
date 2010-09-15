import datetime
from os.path import basename

from django.conf import settings
from django.contrib.comments.models import BaseCommentAbstractModel
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals

#
# Comments
#

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

class ExtendedComment(BaseCommentAbstractModel):
  user = models.ForeignKey(User)
  published = models.DateTimeField('Date Published', auto_now_add=True)
  comment = models.TextField('comment', max_length=COMMENT_MAX_LENGTH)
  #file = models.ForeignKey('ExtendedCommentFile', null=True, blank=True)

  #I'm not sure if this class is really necessary, but the normal comment
  #model has it so better safe than sorry
  class Meta:
    ordering = ('published',)
    verbose_name = ('comment')
    verbose_name_plural = ('comments')

  def __unicode__(self):
    return "%s: %s..." % (self.user, self.comment[:50])

  def save(self, *args, **kwargs):
    if self.published is None:
      self.published = datetime.datetime.now()
    super(ExtendedComment, self).save(*args, **kwargs)

  def get_absolute_url(self, anchor_pattern="#c%(id)s"):
    return "/posts/%s/#c%s" % (self.object_pk, self.id)

  def get_as_text(self):
    d = {
      'user': self.user,
      'date': self.published,
      'comment': self.comment,
      'domain': self.site.domain,
      'url': self.get_absolute_url()
    }
    return 'Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s' % d

#
# Comment Files
#

class ExtendedCommentFile(models.Model):
  def get_upload_path(self, filename):
    return 'uploads/comments/%s/%s' % (self.parent.pk, filename)
  
  file = models.FileField(upload_to=get_upload_path, null=True, blank=True)
  parent = models.ForeignKey(ExtendedComment)

  def __unicode__(self):
    return basename('%s' % (self.file,))

#
# Signals
#

def sanitize_comment(sender, instance, **kwargs):
  #p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
  #instance.comment = p.parse(instance.comment).childNodes[0].childNodes[1].toxml()[6:-7]
  pass

signals.pre_save.connect(sanitize_comment, sender=ExtendedComment)
