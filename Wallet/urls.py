from django.urls import path

from .views import BTCWalletAPI

urlpatterns = [
    path('wallet-info/', BTCWalletAPI.as_view())
]