from django.contrib.syndication.views import Feed
from benchmarks.posts.models import Post
from django.utils.feedgenerator import Atom1Feed

class RssPostsFeed(Feed):
  title = "RSRG Benchmarks Feed"
  link = "/"
  description = "Notification of new feeds posted to the Reusable Software Research Group Benchmarks website."

  def items(self):
    return Post.objects.order_by('-published')[:20]

  def item_title(self, item):
    return item.title

  def item_description(self, item):
    #not 100% sure this is right
    return item.body

class AtomPostsFeed(RssPostsFeed):
  feed_type = Atom1Feed
  subtitle = RssPostsFeed.description
