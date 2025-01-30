from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('wallet/add-balance/', views.AddBalanceView.as_view(), name='add_balance'),
    path('transactions/create/', views.CreateTransactionView.as_view(), name='create_transaction'),
    path('transactions/', views.ListTransactionsView.as_view(), name='list_transactions'),
]