from benchmarks.extended_comments.models import ExtendedComment
from benchmarks.posts.models import Post
from benchmarks.qsseq import QuerySetSequence
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
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

    profile = obj.get_profile()

    lst = Post.objects.filter(author=obj)

    if profile.commentResponseSubscribe:
      for comment in ExtendedComment.objects.filter(user=obj):
        post = Post.objects.get(pk=comment.object_pk)
        lst = QuerySetSequence(lst, ExtendedComment.objects.for_model(post))

    if profile.ownPostCommentSubscribe:
      for post in Post.objects.filter(author=obj):
        lst = QuerySetSequence(lst, ExtendedComment.objects.for_model(post))

    #I think Colin is doing something with groups, I'll finish this
    #after he's done
    if profile.groupPostSubscribe:
      pass

    if profile.allProblemSubscribe:
      lst = QuerySetSequence(lst, Post.objects.filter(category='R'))

    return lst.unique().order_by('-published')[:20]

  def item_title(self, item):
    if item.__class__ == Post:
      return item.title
    else:
      return "Comment"

  def item_description(self, item):
    if item.__class__ == Post:
      return item.body
    else:
      return item.get_as_text()

class AtomPersonalizedFeed(RssPersonalizedFeed):
  feed_type = Atom1Feed
  subtitle = RssPostsFeed.description
