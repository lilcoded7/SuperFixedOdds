import requests
import base64
import hmac
import hashlib
from django.conf import settings


class NaloPayConf:
    baseUrl = "https://api.nalopay.com"

    def __init__(self):
        self.merchant_id = settings.MERCHANT_ID
        self.merchant_secret = settings.MERCHANT_SECRET
        self.username = settings.MERCHANT_USERNAME
        self.password = settings.MERCHANTS_PASSWORD
        self.callback_url = 'http://127.0.0.1:8000'

    def _create_basic_auth_token(self):
        credentials = f"{self.username}:{self.password}"
        return base64.b64encode(credentials.encode()).decode()

    def generate_transfer_token(self):
        url = f"{self.baseUrl}/clientapi/generate-payment-token/"

        headers = {
            "Authorization": f"Basic {self._create_basic_auth_token()}",
            "Content-Type": "application/json",
        }

        payload = {
            "merchant_id": self.merchant_id
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["data"]["token"]

    def _generate_hash(self, account_number, amount, reference):
        message = f"{self.merchant_id}{account_number}{amount}{reference}"
        return hmac.new(
            self.merchant_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def get_network(self, phone_number: str) -> str:
        """ Determines the network based on the phone number prefix. """
        prefix = phone_number[:3]
        mtn = ["024", "054", "025", "053", "054", "055", "059"]
        vod = ["020", "050"]
        atl = ["027", "057", "026", "056"]
        if prefix in mtn:
            return "MTN"
        elif prefix in vod:
            return "VDF"
        elif prefix in atl:
            return "ATL"
        else:
            return "UNKNOWN"


    def collect_payment(self, tx):
        token = self.generate_transfer_token()

        url = f"{self.baseUrl}/clientapi/collection/"

        network = self.get_network(tx.phone)

        trans_hash = self._generate_hash(
            account_number=tx.phone,
            amount=tx.amount,
            reference=tx.transaction_id
        )

        headers = {
            "Content-Type": "application/json",
            "token": token
        }

        data = {
            "merchant_id": self.merchant_id,
            "service_name": "MOMO_TRANSACTION",
            "trans_hash": trans_hash,
            "account_number": tx.phone,
            "account_name": 'account_name' or 'pending',
            "network": network,
            "amount": tx.amount,
            "reference": tx.transaction_id,
            "callback": self.callback_url,
        }

        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()