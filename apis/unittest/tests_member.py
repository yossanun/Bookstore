from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from apis.models import Member


class MemberView(TestCase):
    fixtures = ['apis/fixtures/member.json']

    def test_member_list(self):
        client = APIClient()
        response = client.get('/api/members/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_member(self):
        payload = {
            'first_name': 'Customer',
            'last_name': 'Test'
        }
        response = self.client.post('/api/members/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_member_detail(self):
        client = APIClient()
        response = client.get('/api/members/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_member(self):
        payload = {
            'first_name': 'Customer',
            'last_name': 'Test'
        }
        url = '/api/members/1/'
        response = self.client.patch(url, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], payload['first_name'])
        self.assertEqual(response.data['last_name'], payload['last_name'])

    def test_delete_member(self):
        member = Member.objects.get(id=1)
        url = '/api/members/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
