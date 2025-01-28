from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class WalletTestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_wallet_balance(self):
        response = self.client.get('/wallet/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
