import requests
from django.conf import settings
from payments.models import PaymentTransaction

class SSLCommerzService:
    def __init__(self):
        self.store_id = settings.SSLCOMMERZ_STORE_ID
        self.store_pass = settings.SSLCOMMERZ_STORE_PASS
        self.init_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"

    def create_payment(self, order):
        payload = {
            "store_id": self.store_id,
            "store_passwd": self.store_pass,
            "total_amount": str(order.total_price),
            "currency": "BDT",
            "tran_id": str(order.id),
            "success_url": settings.SSL_SUCCESS_URL,
            "fail_url": settings.SSL_FAIL_URL,
            "cancel_url": settings.SSL_CANCEL_URL,
            "cus_email": order.user.email,
        }
        r = requests.post(self.init_url, data=payload)
        data = r.json()
        return data.get("GatewayPageURL")