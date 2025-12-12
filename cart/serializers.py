# File: cart/serializers.py
from rest_framework import serializers

class CartItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
