from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient
from apis.models import Book


class BookView(TestCase):
    fixtures = ['apis/fixtures/book.json', 'apis/fixtures/author.json']

    def test_book_list(self):
        client = APIClient()
        response = client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        payload = {
            'name': 'Book Test',
            'price': 200,
            'point': 20,
            'author': 1
        }
        response = self.client.post('/api/books/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_detail(self):
        client = APIClient()
        response = client.get('/api/books/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch(self):
        payload = {
            'name': 'Book Test',
            'price': 300,
            'point': 30,
            'author': 1
        }
        response = self.client.patch('/api/books/2/', payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(id=2)
        self.assertEqual(book.name, payload['name'])
        self.assertEqual(book.price, payload['price'])
        self.assertEqual(book.point, payload['point'])

    def test_delete(self):
        book = Book.objects.get(id=2)
        response = self.client.delete('/api/books/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
