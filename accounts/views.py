from rest_framework import generics, permissions, authentication
from rest_framework.views import APIView, Response, Request, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from accounts.models import Account
from accounts.serializers import AccountSerializer, LoginSerializer


class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountNewestView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        num = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:num]


class LoginView(APIView):
    def post(self, request: Request):
        serialized = LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        user = authenticate(**serialized.data)

        print(user)

        if not user:
            return Response(
                {"detail": "invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"Token": token.key}, status=status.HTTP_200_OK)
