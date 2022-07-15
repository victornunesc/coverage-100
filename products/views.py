from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from accounts.models import Account

from products.models import Product
from products.permissions import IsSeller
from products.serializers import GetProductSerializer, ProductSerializer


class ProductView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsSeller]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        return serializer.save(seller_id=self.request.user.id)


class ProductIdView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer
