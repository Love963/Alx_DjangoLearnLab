from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from .models import Post, Comment

class PostsCommentsFeedTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.client.login(username='user1', password='pass123')

        # Create a sample post
        self.post = Post.objects.create(author=self.user, title="Test Post", content="Some content")
        # Create a sample comment
        self.comment = Comment.objects.create(post=self.post, author=self.user, content="Nice post!")

    def test_create_post(self):
        url = reverse('post-list')  
        data = {'title': 'New Post', 'content': 'Content of new post'}
        response = self.client.post(url, data, format='json', follow=True) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_update_permission(self):
        self.client.logout()
        self.client.login(username='user2', password='pass123')
        url = reverse('post-detail', args=[self.post.id]) 
        data = {'title': 'Hacked Post'}
        response = self.client.put(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment(self):
        url = reverse('comment-list') 
        data = {'post': self.post.id, 'content': 'Great!'}
        response = self.client.post(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_update_permission(self):
        self.client.logout()
        self.client.login(username='user2', password='pass123')
        url = reverse('comment-detail', args=[self.comment.id]) 
        data = {'content': 'Edited by someone else'}
        response = self.client.put(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_feed_posts(self):
        self.user2.following.add(self.user)
        self.client.logout()
        self.client.login(username='user2', password='pass123')
        url = reverse('feed')  
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
