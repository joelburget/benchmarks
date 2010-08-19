
from django.test import TestCase
from django.test import Client
from django import template
from django.db.models import get_model

class Testmaker(TestCase):

    #fixtures = ["posts_testmaker"]


    def test_posts_128218141461(self):
        r = self.client.get('/posts/', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['item']), u'work please (joelburget, osu)')
    def test_posts1_128218141771(self):
        r = self.client.get('/posts/1/', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['item']), u'work please (joelburget, osu)')
    def test_commentspost_128218142567(self):
        r = self.client.post('/comments/post/', {'comment': 'here's a comment', 'file': '', 'timestamp': '1282181417', 'object_pk': '1', 'security_hash': '010deb3201bc8ef78acfdb5926f29445d394c133', 'content_type': 'posts.post', 'csrfmiddlewaretoken': '7079d76170014d102d1feebf0ed5cea4', 'honeypot': '', })
    def test__128218142636(self):
        r = self.client.get('/', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['item']), u'work please (joelburget, osu)')
    def test_posts1_128218143005(self):
        r = self.client.get('/posts/1/', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['item']), u'work please (joelburget, osu)')
