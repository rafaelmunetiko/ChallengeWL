from django.urls import path
from . import views

urlpatterns = [
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('wallet/add-balance/', views.AddBalanceView.as_view(), name='add_balance'),
]
