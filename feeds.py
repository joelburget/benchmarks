from django.contrib.syndication.views import Feed
from benchmarks.posts.models import Post
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from benchmarks.extended_comments.models import ExtendedComment
from django.db.models import Q

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

class RssPersonalizedFeed(Feed):
  link = "/"
  description = "Personalized notification of new posts and responses on the Reusable Software Research Group Benchmarks website."

  def get_object(self, request, uname):
    return get_object_or_404(User, username=uname)

  def title(self, obj):
    return "RSRG Benchmarks Feed for %s %s" % (obj.first_name, obj.last_name)

  def items(self, obj):
    #here we want to return the post objects which obj authored
    #or commented on that have updates,
    #as well as any new posts

    lst = Post.objects.filter(author=obj)
    for comment in ExtendedComment.objects.filter(user=obj):
      lst = lst | Post.objects.filter(pk=comment.object_pk)

    return lst.order_by('-published')[:20]

  def item_title(self, item):
    return item.title

  def item_description(self, item):
    #not 100% sure this is right
    return item.body

class AtomPersonalizedFeed(RssPersonalizedFeed):
  feed_type = Atom1Feed
  subtitle = RssPostsFeed.description
