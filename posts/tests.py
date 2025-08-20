from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Post

User = get_user_model()

class PostCommentAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(author=self.user, title="Test Post", content="Post content")

    def test_create_post(self):
        response = self.client.post("/api/posts/", {"title": "New Post", "content": "Some text"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], "user1")

    def test_update_own_post(self):
        response = self.client.patch(f"/api/posts/{self.post.id}/", {"content": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_others_post(self):
        self.client.force_authenticate(user=self.user2)  # switch user
        response = self.client.patch(f"/api/posts/{self.post.id}/", {"content": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment(self):
        response = self.client.post("/api/comments/", {"post": self.post.id, "content": "Nice!"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], "user1")
