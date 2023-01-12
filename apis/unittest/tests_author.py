from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient
from apis.models import Author


class AuthorView(TestCase):
    fixtures = ['apis/fixtures/author.json']

    # @override_settings(IS_EXPLORE=False)
    # def test_author_list_not_login(self):
    #     response = self.client.get('/api/authors/')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_list(self):
        client = APIClient()
        # user = User.objects.get(id=1)
        # client.force_authenticate(user=user)
        response = client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_author(self): 
        payload = {
            'first_name': 'Author',
            'last_name': 'Test'
        }
        response = self.client.post('/api/authors/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_author_detail(self):
        client = APIClient()
        # user = User.objects.get(id=1)
        # client.force_authenticate(user=user)
        response = client.get(f'/api/authors/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_author(self):
        payload = {
            'first_name': 'Author',
            'last_name': 'Test'
        }
        url = '/api/authors/1/'
        response = self.client.patch(url, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author = Author.objects.filter(id=1).first()
        self.assertEqual(author.first_name, payload['first_name'])
        self.assertEqual(author.last_name, payload['last_name'])

    def test_delete_author(self):
        author = Author.objects.get(id=1)
        url = '/api/authors/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)