import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wallet_project.settings')
django.setup()

from wallet.models import CustomUser, Wallet

# Criar usuários fictícios
user1 = CustomUser.objects.create_user(username='rafael', email='rafael@email.com', password='123456')
wallet1 = Wallet.objects.create(user=user1, balance=1000.00)

print("Dados populados com sucesso!")
