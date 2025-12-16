from django.urls import path
from .views import CreateStripeSessionView, StripeWebhookView

urlpatterns = [
    path('stripe/create-session/', CreateStripeSessionView.as_view(), name='stripe_create_session'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),
]