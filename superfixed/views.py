from django.shortcuts import render
from rest_framework import generics
from superfixed.serializers import SlipSerializer, PurchaseBetSlipSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from superfixed.models.slips import Betslip, Transaction
from rest_framework.response import Response
from superfixed.payment_config import NaloPayConf
from superfixed.models.brandaccounts import BrandAccount
from rest_framework.exceptions import NotFound
from django.utils import timezone
from decimal import Decimal
import uuid

pay = NaloPayConf()

# Create your views here.


def generate_reference():
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    random_part = uuid.uuid4().hex[:6].upper()
    return f"CodedPay{timestamp}{random_part}"


class BetSlipAPIView(generics.GenericAPIView):
    serializer_class = SlipSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        active_slips = Betslip.objects.filter(is_active=True)
        serializer = self.serializer_class(active_slips, many=True)
        return Response(serializer.data, status=200)


class PurchaseBetSlipAPIView(generics.GenericAPIView):
    serializer_class = PurchaseBetSlipSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        amount = Decimal(data.get("amount"))

        slip = Betslip.objects.first()

        transaction = Transaction.objects.create(
            slip=slip,
            phone=data.get("phone_number"),
            status="pending",
            amount=amount,
            transaction_id=generate_reference(),
        )
        process_payment = pay.collect_payment(transaction)

        return Response({"data": process_payment}, status=200)


class BrandSlipAPIView(generics.GenericAPIView):
    serializer_class=SlipSerializer
    permission_classes = [AllowAny]


    def get(self, request):

        brand_name = request.query_params.get('brand_name')

        try:
            brand = BrandAccount.objects.get(abbr=brand_name)
        except BrandAccount.DoesNotExist:
            raise NotFound("Brand account does not exist")
        
        slips = Betslip.objects.filter(brand=brand, is_active=True)

        return Response(
            {
                'slips':SlipSerializer(slips, many=True).data
            }
        )



