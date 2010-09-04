"""
Group views and GroupProfile model tests
"""

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.test.client import Client

class GroupsTest(TestCase):
  fixtures = ['users.json', 'groups.json']

  def setUp(self):
    self.group = Group.objects.get(pk=1)
    self.url = self.group.groupprofile.get_absolute_url()

    self.user = User.objects.get(pk=1)
    username = self.user.username  # password is same as username

    self.c = Client()
    self.c.login(username=username,password=username)

  # Model Tests

  def test_group_profile_creation(self):
    """Tests that group profiles are created when groups are saved"""
    group = Group(name="Test Group")
    group.save()
    self.failIfEqual(group.groupprofile, None)

  # View Tests

  def test_index_groups(self):
    """Tests that groups are listed"""
    resp = self.c.get('/groups/')
    found = resp.content.index(self.group.name) >= 0
    self.failIfEqual(found, False)

  def test_view_group(self):
    """Tests that group URLs work"""
    resp = self.c.get(self.url)
    found = resp.content.index(self.group.name)
    self.failIfEqual(found, -1)

  def test_join_group(self):
    """Tests that a user can join a group"""
    resp = self.c.post('/groups/join/', { 'groupid':self.group.pk })
    self.assertEqual(self.user.get_profile().group, self.group)

  def test_leave_group(self):
    """Tests that a user can leave a group"""
    resp = self.c.post('/groups/leave/', { 'groupid':self.group.pk })
    self.assertEqual(self.user.get_profile().group, None)
