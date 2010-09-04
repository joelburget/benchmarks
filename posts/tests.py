"""
Posts, etc. tests
"""

from posts.models import *
from django.test import TestCase
from django.test.client import Client

class PostsTest(TestCase):
  fixtures = ['users.json', 'groups.json', 'posts.json']

  def setUp(self):
    self.user = User.objects.get(pk=1)
    self.url = self.user.get_absolute_url()
    username = self.user.username  # password is same as username

    self.c = Client()
    self.c.login(username=username,password=username)

  # Model tests

  def test_no_revisions(self):
    """Tests that revisions on a post without any returns itself"""
    post = Post.objects.all()[0]
    self.failUnlessEqual([post], post.get_revisions())

  def test_some_revisions(self):
    """Tests that revisions on a post are returned"""
    post = Post.objects.all()[0]
    prev = PostRevision(author=post.author, group=post.group, body='body!')
    post.previous = prev
    self.failUnlessEqual([post, prev], post.get_revisions())

  def test_sanitize(self):
    """Tests that post bodies are sanitized"""
    post = Post(title='Boo', body='Hello! <script>alert();</script>',
                author=User.objects.all()[0], group=Group.objects.all()[0])
    post.save()
    self.failUnlessEqual(post.body, 'Hello! &lt;script&gt;alert();&lt;/script&gt;')

  # View tests

  def test_posts_index(self):
    """Tests the posts index page"""
    r = self.c.get('/posts/')

    # Note: truncates titles because we only display `x` words
    found = r.content.index(Post.objects.get(pk=1).title[:10]) != -1 and \
            r.content.index(Post.objects.get(pk=2).title[:10]) != -1 and \
            r.content.index(Post.objects.get(pk=3).title[:10]) != -1
    self.failIfEqual(found, False)

  def test_post_detail(self):
    """Tests the post detail view page"""
    post = Post.objects.all()[0]
    r = self.c.get(post.get_absolute_url())
    found = r.content.index(post.title)
    self.failIfEqual(found, -1)
