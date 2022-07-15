from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from accounts.models import Account
from core.mixins import SerializerByMethodMixin

from products.models import Product
from products.permissions import IsProductOwner, IsSeller
from products.serializers import GetProductSerializer, ProductSerializer


class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsSeller]

    queryset = Product.objects.all()
    serializer_map = {"POST": ProductSerializer, "GET": GetProductSerializer}

    def perform_create(self, serializer):
        return serializer.save(seller_id=self.request.user.id)


class ProductIdView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsProductOwner]

    queryset = Product.objects.all()
    serializer_map = {"PATCH": ProductSerializer, "GET": GetProductSerializer}
