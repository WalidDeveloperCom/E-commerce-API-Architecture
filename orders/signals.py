from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Order, OrderItem
from products.models import Product

@receiver(post_save, sender=Order)
def reduce_stock_on_order(sender, instance, created, **kwargs):
    if created and instance.status == "CONFIRMED":
        for item in instance.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()


@receiver(pre_delete, sender=Order)
def restore_stock_on_order_delete(sender, instance, **kwargs):
    for item in instance.items.all():
        product = item.product
        product.stock += item.quantity
        product.save()
