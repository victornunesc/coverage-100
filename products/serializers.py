from rest_framework import serializers
from accounts.serializers import AccountSerializer
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["is_active"]


class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
