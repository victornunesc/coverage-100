from enum import unique
from rest_framework.views import Request
from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["date_joined"]

    def create(self, validated_data: dict):
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
