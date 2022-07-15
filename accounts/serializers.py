from enum import unique
from rest_framework.views import Request
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

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


class AccountManagement(serializers.ModelSerializer):
    class Meta:
        model = Account
        extra_kwargs = {
            "password": {"write_only": True},
        }
        exclude = [
            "is_superuser",
            "date_joined",
            "groups",
            "user_permissions",
            "last_login",
        ]

    def validate_password(self, value):
        password = make_password(value)
        return password


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
