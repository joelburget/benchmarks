from django import forms
from django.contrib.comments.forms import CommentForm
from benchmarks.extended_comments.models import ExtendedComment

class ExtendedCommentForm(CommentForm):
  file = forms.FileField(required=False)

  def get_comment_model(self):
    return ExtendedComment

  def get_comment_create_data(self):
    data = super(ExtendedCommentForm, self).get_comment_create_data()
    data['file'] = self.cleaned_data['file']
    return data
