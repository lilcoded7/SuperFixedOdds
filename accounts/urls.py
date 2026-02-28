from django.urls import path
from accounts.views import LoginAccountAPIView


urlpatterns = [
    path('login/', LoginAccountAPIView.as_view(), name='login')
]