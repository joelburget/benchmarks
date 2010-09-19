from haystack import indexes, site
from benchmarks.posts.models import Post

class PostIndex(indexes.RealTimeSearchIndex):
  text = indexes.CharField(document=True, use_template=True)
  author = indexes.CharField(model_attr="author")

site.register(Post, PostIndex)
