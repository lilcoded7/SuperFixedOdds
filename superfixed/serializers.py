from rest_framework import serializers
from superfixed.models.slips import *
from superfixed.models.brandaccounts import BrandAccount, Customization
from accounts.serializers import UserSerializer


class BrandAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model=BrandAccount
        fields = '__all__'


class CustomizationAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customization
        fields = '__all__'

class AccountCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customization
        fields='__all__'


class SlipSerializer(serializers.ModelSerializer):
    class Meta:
        model=Betslip
        fields = "__all__"


class PurchaseBetSlipSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("invalid phone number")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("amount should be greater than 0")
        return value
    
