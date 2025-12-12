from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import CartItemSerializer
from .redis_client import r
# Create your views here.

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = r.get_cart(request.user.id)
        return Response(cart)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = r.get_cart(request.user.id) or {}
        pid = str(serializer.validated_data['product_id'])
        qty = serializer.validated_data['quantity']
        cart[pid] = cart.get(pid, 0) + qty
        r.set_cart(request.user.id, cart)
        return Response(cart, status=status.HTTP_201_CREATED)

    def delete(self, request):
        item = request.data.get('product_id')
        cart = r.get_cart(request.user.id) or {}
        if item and str(item) in cart:
            cart.pop(str(item))
            r.set_cart(request.user.id, cart)
        return Response(cart)
