"""
User views and UserProfile tests
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

class UsersTest(TestCase):
  fixtures = ['users.json', 'groups.json']

  def setUp(self):
    self.user = User.objects.get(pk=1)
    self.url = self.user.get_absolute_url()
    username = self.user.username  # password is same as username

    self.c = Client()
    self.c.login(username=username,password=username)

  # Model tests

  def test_user_profile_creation(self):
    """Tests that user profiles are created for all Users"""
    user = User(username='roy', password='batty')
    user.save()
    self.failIfEqual(user.get_profile(), None)

  def test_no_name(self):
    """Tests that users without names have display names of usernames"""
    user = User(username='ronald', password='mcdonald')
    user.save()
    self.assertEqual('ronald', user.get_profile().get_display_name())

  def test_real_name(self):
    """Tests that users with names have display names including them"""
    user = User(username='the', password='intersect')
    user.first_name = 'Chuck'
    user.last_name = 'Bartowski'
    user.save()
    self.assertEqual('Chuck Bartowski', user.get_profile().get_display_name())

  # View tests

  def test_user_index(self):
    """Tests that the user index page displays users"""
    r = self.c.get('/users/')
    found = r.content.index(self.user.username)
    self.failIfEqual(found, -1)

  def test_show_user(self):
    """Tests that user profile pages work"""
    r = self.c.get(self.url)
    found = r.content.index(self.user.username)
    self.failIfEqual(found, -1)

  def test_edit_user(self):
    """Tests that users can edit their own profiles"""
    r = self.c.get('%sedit/' % self.user.get_absolute_url())
    found = r.content.index('editForm')
    self.failIfEqual(found, -1)

  def test_edit_user_permissions(self):
    """Tests that users can't edit profiles other than their own"""
    user = User(username="jeff")
    user.save()
    r = self.c.get('%sedit/' % user.get_absolute_url())
    found = r.content.index('Oops!')
    self.failIfEqual(found, -1)
