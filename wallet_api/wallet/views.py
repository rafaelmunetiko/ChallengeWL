from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class WalletView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

class AddBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        wallet = Wallet.objects.get(user=request.user)
        amount = request.data.get('amount')
        wallet.balance += float(amount)
        wallet.save()
        return Response({"message": "Balance updated successfully!"})
