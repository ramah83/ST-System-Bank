from django.urls import path

from .views import (
    DepositMoneyView, 
    WithdrawMoneyView, 
    TransactionRepostView,
    UserSearchView,
    TransactionSearchView
)


app_name = 'transactions'


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("report/", TransactionRepostView.as_view(), name="transaction_report"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),
    path("search/users/", UserSearchView.as_view(), name="user_search"),
    path("search/transactions/", TransactionSearchView.as_view(), name="transaction_search"),
]
