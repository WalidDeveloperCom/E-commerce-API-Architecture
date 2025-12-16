import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(order_id, amount, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price_data':{
            'currency':'usd',
            'product_data':{'name':f'Order {order_id}'},
            'unit_amount': int(float(amount)*100),
        },
         'quantity':1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={'order_id': str(order_id)})
    return session