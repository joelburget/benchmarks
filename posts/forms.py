from django.forms import ModelForm

from benchmarks.posts.models import Post

class PostForm(ModelForm):
  class Meta():
    model = Post
