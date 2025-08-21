# posts/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class PostsCommentsFeedTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", password="pass1234")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

        self.posts_url = "/posts/"
        self.comments_url = "/comments/"
        self.feed_url = "/feed/feed/"

        self.post = Post.objects.create(author=self.user1, title="Post1", content="Content1")
        self.comment = Comment.objects.create(author=self.user1, post=self.post, content="Nice post!")

    def test_create_post(self):
        data = {"title": "New Post", "content": "New Content"}
        response = self.client.post(self.posts_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_update_permission(self):
        post2 = Post.objects.create(author=self.user2, title="Other Post", content="Other content")
        url = f"{self.posts_url}{post2.id}/"
        data = {"title": "Hacked", "content": "Hacked content"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment(self):
        data = {"post": self.post.id, "content": "Another comment"}
        response = self.client.post(self.comments_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_update_permission(self):
        comment2 = Comment.objects.create(author=self.user2, post=self.post, content="Other comment")
        url = f"{self.comments_url}{comment2.id}/"
        data = {"content": "Hacked comment"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_feed_posts(self):
        self.user1.following.add(self.user2)
        post2 = Post.objects.create(author=self.user2, title="Followed Post", content="Content2")
        response = self.client.get(self.feed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Followed Post")
