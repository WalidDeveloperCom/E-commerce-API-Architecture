from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from .services.stripe_service import create_checkout_session
from .models import PaymentTransaction


class CreateStripeSessionView(APIView):
permission_classes = [permissions.IsAuthenticated]
def post(self, request):
order_id = request.data.get('order_id')
amount = request.data.get('amount')
success_url = request.data.get('success_url') or 'https://example.com/success'
cancel_url = request.data.get('cancel_url') or 'https://example.com/cancel'
session = create_checkout_session(order_id, amount, success_url, cancel_url)
# create transaction
tx = PaymentTransaction.objects.create(order_id=order_id, payment_gateway='stripe', amount=amount, status='pending', transaction_id=session.id)
return Response({'checkout_url': session.url})


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import stripe


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
authentication_classes = []
permission_classes = []
def post(self, request):
payload = request.body
sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
try:
event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
except Exception as e:
return Response(status=400)
# handle checkout.session.completed
if event['type'] == 'checkout.session.completed':
session = event['data']['object']
order_id = session['metadata'].get('order_id')
# mark transaction
PaymentTransaction.objects.filter(transaction_id=session['id']).update(status='success')
return Response(status=200)