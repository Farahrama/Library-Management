from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Book, Borrowing
from django.utils import timezone
from datetime import date

class BookAPITest(APITestCase):
    def setUp(self):
        Book.objects.all().delete()
        Borrowing.objects.all().delete()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            published_date="2023-01-01",
            copies_available=5
        )

    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1, msg=f"Expected 1 book, got {len(response.data['results'])}: {response.data['results']}")
        self.assertEqual(response.data['results'][0]['title'], 'Test Book')
    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "9876543210123",
            "published_date": "2024-01-01",
            "copies_available": 3
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_checkout_book(self):
        data = {"book_id": self.book.id}
        response = self.client.post('/api/books/checkout/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 4)
        self.assertEqual(Borrowing.objects.count(), 1)

    def test_return_book(self):
        Borrowing.objects.create(user=self.user, book=self.book)
        data = {"book_id": self.book.id}
        response = self.client.post('/api/books/return/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 6)
        borrowing = Borrowing.objects.get(user=self.user, book=self.book)
        self.assertIsNotNone(borrowing.return_date)

    def test_stats(self):
        response = self.client.get('/api/books/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_books'], 1)
        self.assertEqual(response.data['available_copies'], 5)