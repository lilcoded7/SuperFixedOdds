from django.shortcuts import render
from accounts.serializers import LoginSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from superfixed.models.brandaccounts import BrandAccount, Customization
from superfixed.serializers import (
    BrandAccountSerializer,
    CustomizationAccountSerializer,
)

# Create your views here.

from django.contrib.auth import get_user_model

User = get_user_model()


class LoginAccountAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def _validate_user_phone_number(self, phone_number):
        try:
            user = User.objects.get(phone_number=phone_number)
            return user
        except User.DoesNotExist:
            raise ValueError("User does not exist")

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = self._validate_user_phone_number(data.get("phone_number"))

        print(user, " User")

        brand_account = BrandAccount.objects.filter(user=user)

        customization = Customization.objects.filter(brand__in=brand_account)

        if user:
            token = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful!",
                    "tokens": {
                        "access_token": str(token.access_token),
                        "refresh_token": str(token),
                    },
                    "AccountInfo": BrandAccountSerializer(brand_account, many=True).data,
                    "AccountCustomization": CustomizationAccountSerializer(
                        customization, many=True
                    ).data,
                }
            )
