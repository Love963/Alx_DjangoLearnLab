from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Book, Author


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Create an author (without biography if your model doesn’t have it)
        self.author = Author.objects.create(name="Author A")

        # Create a sample book
        self.book = Book.objects.create(
            title="Sample Book",
            author=self.author,
            publication_year=2020,
            #isbn="1234567890123"
        )

        # Store endpoint URLs
        self.list_url = reverse('book-list')       # GET list
        self.create_url = reverse('book-create')   # POST create
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})  # GET detail
        self.update_url = reverse('book-update', kwargs={'pk': self.book.pk})  # PUT/PATCH update
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book.pk})  # DELETE


    def test_book_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Sample Book", str(response.data))


    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'New Book',
            'author': self.author.id,  # Must pass ID for ForeignKey
            'publication_year': 2023,
            #'isbn': '9876543210123'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)


    def test_create_book_unauthenticated(self):
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'publication_year': 2023,
            #'isbn': '9876543210123'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')


    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())


    def test_filter_book_by_title(self):
        response = self.client.get(f'{self.list_url}?title=Sample')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


    def test_search_book_by_author(self):
        response = self.client.get(f'{self.list_url}?search=Author A')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_order_books_by_publication_year(self):
        Book.objects.create(
            title="Older Book",
            author=self.author,
            publication_year=2010,
            # isbn="1111111111111"
        )
        response = self.client.get(f'{self.list_url}?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
