from django.db import models
from django.contrib.comments.models import Comment

class ExtendedComment(Comment):
  file = models.FileField(upload_to='uploads', null=True, blank=True)
