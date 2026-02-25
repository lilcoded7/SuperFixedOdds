from django.urls import path
from superfixed.views import *


urlpatterns = [
    path('betslips/', BetSlipAPIView.as_view(), name='betslips'),
    path('purchase/slip/', PurchaseBetSlipAPIView.as_view(), name='purchase_slip')
    
]