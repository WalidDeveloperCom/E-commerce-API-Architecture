from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from products.services.inventory_service import InventoryService
# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def create_order(self, request):
    cart_items = CartService.get_cart(request.user)

    # validate stock
    InventoryService.validate_cart_items(cart_items)

    # reserve stock
    for item in cart_items:
        InventoryService.reserve_stock(item["product"], item["quantity"])

    # continue order creation...