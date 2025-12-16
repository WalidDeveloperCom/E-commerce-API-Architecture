from django.db import models
import uuid
# Create your models here.

class PaymentTransaction(models.Model):
    STATUS_CHOICES = [('pending','pending'),('success','success'),('failed','failed')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField()
    payment_gateway = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)