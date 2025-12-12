from django.core.exceptions import ValidationError
from products.models import Product

class InventoryService:

    @staticmethod
    def check_stock(product: Product, qty: int):
        if product.stock < qty:
            raise ValidationError(f"Insufficient stock for {product.name}")

    @staticmethod
    def reserve_stock(product: Product, qty: int):
        InventoryService.check_stock(product, qty)
        product.stock -= qty
        product.save()

    @staticmethod
    def release_stock(product: Product, qty: int):
        product.stock += qty
        product.save()

    @staticmethod
    def validate_cart_items(cart_items):
        for item in cart_items:
            InventoryService.check_stock(item["product"], item["quantity"])
