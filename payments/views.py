import stripe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from django.shortcuts import get_object_or_404
from orders.models import Order

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Create Stripe payment intent",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order_number': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={200: 'Payment intent created', 400: 'Bad Request'}
    )
    def post(self, request):
        order_number = request.data.get('order_number')
        
        if not order_number:
            return Response(
                {'error': 'order_number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get order
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        
        # Check if order can be paid
        if order.payment_status != 'pending':
            return Response(
                {'error': 'Order payment is not pending'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(order.total * 100),  # Convert to cents
                currency='usd',
                metadata={
                    'order_number': order.order_number,
                    'user_id': str(request.user.id)
                },
                description=f"Payment for order {order.order_number}",
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            
            return Response({
                'client_secret': intent.client_secret,
                'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                'order_number': order.order_number,
                'amount': order.total
            })
            
        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class PaymentSuccessView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Handle successful payment",
        responses={200: 'Payment successful', 400: 'Bad Request'}
    )
    def post(self, request):
        payment_intent_id = request.data.get('payment_intent_id')
        order_number = request.data.get('order_number')
        
        if not payment_intent_id or not order_number:
            return Response(
                {'error': 'payment_intent_id and order_number are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Retrieve payment intent
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            # Verify payment status
            if intent.status != 'succeeded':
                return Response(
                    {'error': 'Payment not successful'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get order
            order = get_object_or_404(Order, order_number=order_number, user=request.user)
            
            # Update order payment status
            order.payment_status = 'paid'
            order.payment_method = 'stripe'
            order.transaction_id = payment_intent_id
            order.paid_at = timezone.now()
            order.save()
            
            # Update order status to confirmed
            order.status = 'confirmed'
            order.save()
            
            # Trigger order confirmation email (async)
            # send_order_confirmation_email.delay(order.id)
            
            return Response({
                'message': 'Payment successful',
                'order_number': order.order_number,
                'transaction_id': payment_intent_id
            })
            
        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class StripeWebhookView(APIView):
    permission_classes = []
    
    @swagger_auto_schema(
        operation_description="Stripe webhook endpoint",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT),
        responses={200: 'Webhook received'}
    )
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return Response({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return Response({'error': 'Invalid signature'}, status=400)
        
        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            handle_payment_intent_succeeded(payment_intent)
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            handle_payment_intent_failed(payment_intent)
        
        return Response({'status': 'success'})

def handle_payment_intent_succeeded(payment_intent):
    """Handle successful payment from webhook"""
    order_number = payment_intent['metadata'].get('order_number')
    
    if order_number:
        try:
            order = Order.objects.get(order_number=order_number)
            order.payment_status = 'paid'
            order.transaction_id = payment_intent['id']
            order.paid_at = timezone.now()
            order.status = 'confirmed'
            order.save()
        except Order.DoesNotExist:
            pass

def handle_payment_intent_failed(payment_intent):
    """Handle failed payment from webhook"""
    order_number = payment_intent['metadata'].get('order_number')
    
    if order_number:
        try:
            order = Order.objects.get(order_number=order_number)
            order.payment_status = 'failed'
            order.save()
        except Order.DoesNotExist:
            pass