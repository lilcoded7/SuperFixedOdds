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


    def generate_transfer_token(self):
        url = f"{self.baseUrl}/clientapi/generate-payment-token/"

        headers = {
            "Authorization": 'Basic e28ef19a40cb885863362895e7d2c6df09fd417bed99d0138208f280c28152e81772d41303caa8e366d3a4be9ff463ff2002efde1e3db4150d9ed04bf66677f4',
            "Content-Type": "application/json",
        }

        payload = {
            "merchant_id": self.merchant_id
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["data"]["token"]

    def _generate_hash(self, account_number, amount, reference):
        # Format amount to 2 decimal places to match standard currency strings (e.g., "50.00")
        formatted_amount = "{:.2f}".format(float(amount))
        
        # Concatenate exactly as the docs say: merchant_id + account_number + amount + reference
        message = f"{self.merchant_id}{account_number}{formatted_amount}{reference}"
        
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
            return "TELECEL"
        elif prefix in atl:
            return "AT"
        else:
            return "UNKNOWN"


    def collect_payment(self, tx):
        token = self.generate_transfer_token()
        url = f"{self.baseUrl}/clientapi/collection/"
        network = self.get_network(tx.phone)
        
        # Use consistent formatting for both the hash and the payload
        formatted_amount = "{:.2f}".format(float(tx.amount))

        trans_hash = self._generate_hash(
            account_number=tx.phone,
            amount=formatted_amount, # Pass the formatted string
            reference=tx.transaction_id
        )

        headers = {
            "Content-Type": "application/json",
            "token": token
        }

        print(network, ' Network')
        

        data = {
            "merchant_id": self.merchant_id,
            "service_name": "MOMO_TRANSACTION",
            "trans_hash": trans_hash,
            "account_number": tx.phone,
            "account_name": 'pending',
            "network": network,
            "amount": formatted_amount, 
            "reference": tx.transaction_id,
            "callback": self.callback_url,
        }

        response = requests.post(url, json=data, headers=headers, timeout=30)

        print(response.json())
        
        # Debugging: If it still fails, print the response text to see the API's specific error message
        if response.status_code != 200:
            print(f"Error Response: {response.text}")
            
        response.raise_for_status()
        return response.json()