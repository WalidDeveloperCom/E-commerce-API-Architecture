from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, source='product', queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id','product','product_id','quantity','unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','user','total_price','status','items','created_at']
        read_only_fields = ['user','total_price','status','created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user)
        total = 0
        for item in items_data:
            product = item['product']
            qty = item['quantity']
            unit_price = product.price
            OrderItem.objects.create(order=order, product=product, quantity=qty, unit_price=unit_price)
            total += unit_price * qty
            # simple stock decrease
            if product.stock >= qty:
                product.stock -= qty
                product.save()
        order.total_price = total
        order.save()
        return order
