import os
import django

# Definir o caminho correto para o settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallet_api.wallet_api.settings")

# Configurar Django
django.setup()
