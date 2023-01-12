from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal

from apis.models import Transaction, Book


class TransactionView(TestCase):
    fixtures = ['apis/fixtures/transaction.json', 'apis/fixtures/member.json', 'apis/fixtures/book.json', 'apis/fixtures/configuration.json']
    book = Book.objects.get(id=2)

    def test_transaction_list(self):
        client = APIClient()
        response = client.get('/api/transactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_transaction(self):

        # ----- Use Cash and Point Transaction -----
        payload = {
                'member': 1,
                'book': 2,
                'is_use_point': True,
                'is_use_cash': True,
                'use_point': 100,
                'use_cash': 100
            }
        response = self.client.post('/api/transactions/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data['use_point'])+Decimal(response.data['use_cash']), self.book.price)

    def test_create_transaction_with_cash(self):

        # ----- Use Cash Transaction -----
        book = Book.objects.filter(id=1).first()
        payload = {
                'member': 1,
                'book': 2,
                'is_use_point': False,
                'is_use_cash': True,
                'use_point': '0',
                'use_cash': '200'
            }
        response = self.client.post('/api/transactions/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data['use_cash']), self.book.price)

    def test_create_transaction_with_point(self):
        
        # ----- Use Point Transaction -----
        payload = {
                'member': 1,
                'book': 2,
                'is_use_point': True,
                'is_use_cash': False,
                'use_point': '200',
                'use_cash': '0'
            }
        response = self.client.post('/api/transactions/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data['use_point']), self.book.price)

    def test_transaction_detail(self):
        client = APIClient()
        response = client.get('/api/transactions/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_transaction(self):
        url = '/api/transactions/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

