from django.shortcuts import render
from rest_framework import generics, permissions, authentication
from rest_framework.views import APIView, Response, Request

from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountNewestView(generics.ListAPIView):
    ...


class LoginView(APIView):
    ...
