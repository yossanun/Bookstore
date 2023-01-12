from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from decimal import Decimal

from apis.models import Configuration


class ConfigurationView(TestCase):
    fixtures = ['apis/fixtures/configuration.json']

    def test_configuration_list(self):
        client = APIClient()
        response = client.get('/api/configurations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_configuration(self):
        payload = {
            'name': 'point-1',
            'value': 100
        }
        response = self.client.post('/api/configurations/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], payload['name'])
        self.assertEqual(Decimal(response.data['value']), payload['value'])

    def test_configuration_detail(self):
        client = APIClient()
        response = client.get('/api/configurations/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_configuration(self):
        payload = {
            'name': 'promotion-1',
            'value': 10.000
        }
        url = '/api/configurations/1/'
        response = self.client.patch(url, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], payload['name'])
        self.assertEqual(Decimal(response.data['value']), payload['value'])

    def test_delete_configuration(self):
        configuration = Configuration.objects.get(id=1)
        url = '/api/configurations/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
