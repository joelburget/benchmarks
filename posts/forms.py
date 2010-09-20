from django.utils.safestring import mark_safe
from django.forms import ModelForm

from benchmarks.posts.models import Post

class PostForm(ModelForm):
  class Meta:
    model = Post

  def __init__(self, *args, **kwargs):
    super(ModelForm, self).__init__(*args, **kwargs)
    self.fields['body'].label = mark_safe('Body (We accept LaTeX like <span style="font-family:monospace; font-size: 1.2em;">$$x^2$$</span>, and <a href="http://en.wikipedia.org/wiki/Markdown#Syntax_examples" target="_blank">Markdown</a>):')
