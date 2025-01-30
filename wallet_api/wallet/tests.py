from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Wallet, Transaction

class WalletTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.wallet = Wallet.objects.create(user=self.user, balance=1000.00)
        self.client.force_authenticate(user=self.user)

    def test_wallet_balance(self):
        response = self.client.get('/api/wallet/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '1000.00')

    def test_add_balance(self):
        response = self.client.post('/api/wallet/add-balance/', {'amount': 500.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1500.00)

    def test_create_transaction(self):
        receiver = get_user_model().objects.create_user(username='receiver', password='receiverpass')
        receiver_wallet = Wallet.objects.create(user=receiver, balance=500.00)

        response = self.client.post('/api/transactions/create/', {
            'receiver': 'receiver',
            'amount': 200.00
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.wallet.refresh_from_db()
        receiver_wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 800.00)
        self.assertEqual(receiver_wallet.balance, 700.00)

    def test_list_transactions(self):
        receiver = get_user_model().objects.create_user(username='receiver', password='receiverpass')
        receiver_wallet = Wallet.objects.create(user=receiver, balance=500.00)
        Transaction.objects.create(sender=self.wallet, receiver=receiver_wallet, amount=200.00)

        response = self.client.get('/api/transactions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)