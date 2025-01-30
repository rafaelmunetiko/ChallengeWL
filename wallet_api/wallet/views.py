from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser, Wallet, Transaction
from .serializers import UserSerializer, WalletSerializer, TransactionSerializer

# Endpoint para criar um usuário
class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Wallet.objects.create(user=user)  # Cria uma carteira para o novo usuário
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint para autenticação (gerar token JWT)
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

# Endpoint para criar uma transferência entre usuários
class CreateTransactionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sender_wallet = Wallet.objects.get(user=request.user)
        receiver_username = request.data.get('receiver')
        amount = float(request.data.get('amount'))

        if sender_wallet.balance < amount:
            return Response({'error': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = CustomUser.objects.get(username=receiver_username)
            receiver_wallet = Wallet.objects.get(user=receiver)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuário receptor não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        sender_wallet.balance -= amount
        receiver_wallet.balance += amount
        sender_wallet.save()
        receiver_wallet.save()

        transaction = Transaction.objects.create(
            sender=sender_wallet,
            receiver=receiver_wallet,
            amount=amount
        )

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

# Endpoint para listar transferências com filtro por período
class ListTransactionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        wallet = Wallet.objects.get(user=request.user)

        transactions = Transaction.objects.filter(sender=wallet)
        if start_date and end_date:
            transactions = transactions.filter(created_at__range=[start_date, end_date])

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)