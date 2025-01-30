import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallet_api.settings")
django.setup()

def populate_db():
    User = get_user_model()
    
    # Criar usuários
    user1 = User.objects.create_user(username='user1', password='password1')
    user2 = User.objects.create_user(username='user2', password='password2')

    # Criar carteiras
    wallet1 = Wallet.objects.get(user=user1)
    wallet2 = Wallet.objects.get(user=user2)

    # Adicionar saldo
    wallet1.balance = 1000.00
    wallet2.balance = 500.00
    wallet1.save()
    wallet2.save()

    # Criar transações
    Transaction.objects.create(sender=wallet1, receiver=wallet2, amount=200.00)
    Transaction.objects.create(sender=wallet2, receiver=wallet1, amount=50.00)

    print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    populate_db()