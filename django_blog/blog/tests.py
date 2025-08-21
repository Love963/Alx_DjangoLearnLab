from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
# Create your tests here.

class PostCrudTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user('alice', 'a@a.com', 'pass12345')
        self.other  = User.objects.create_user('bob', 'b@b.com', 'pass12345')
        self.post = Post.objects.create(title='Hello', content='World', author=self.author)

    def test_list_view(self):
        resp = self.client.get(reverse('post-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Hello')

    def test_detail_view(self):
        resp = self.client.get(reverse('post-detail', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'World')

    def test_create_requires_login(self):
        resp = self.client.get(reverse('post-create'))
        self.assertNotEqual(resp.status_code, 200)  # redirected to login
        self.client.login(username='alice', password='pass12345')
        resp = self.client.post(reverse('post-create'), {'title': 'New', 'content': 'Post'})
        self.assertEqual(Post.objects.count(), 2)
        self.assertRedirects(resp, Post.objects.latest('id').get_absolute_url())

    def test_only_author_can_update(self):
        self.client.login(username='bob', password='pass12345')
        resp = self.client.post(reverse('post-edit', args=[self.post.pk]), {'title': 'Hack', 'content': 'Nope'})
        self.assertNotEqual(resp.status_code, 302)      # should be 403
        self.client.login(username='alice', password='pass12345')
        resp = self.client.post(reverse('post-edit', args=[self.post.pk]), {'title': 'Updated', 'content': 'Good'})
        self.assertEqual(resp.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated')
