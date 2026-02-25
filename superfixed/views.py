from django.shortcuts import render
from rest_framework import generics
from superfixed.serializers import SlipSerializer, PurchaseBetSlipSerializer
from rest_framework.permissions import AllowAny
from superfixed.models.slips import Betslip, Transaction
from rest_framework.response import Response
from superfixed.payment_config import NaloPayConf
from django.utils import timezone
import uuid

pay = NaloPayConf()

# Create your views here.

def generate_reference():
    timestamp= timezone.now().strftime("%Y%m%d%H%M%S")
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

        slip = Betslip.objects.first()

        transaction =Transaction.objects.create(
            slip=slip, 
            phone=data.get('phone_number'),
            status='pending',
            amount=data.get('amount'),
            transaction_id=generate_reference()
        )
        process_payment = pay.collect_payment(transaction)

        return Response({
            
            'data':process_payment
        }, status=200
        )




