import json
import stripe
from django.http import JsonResponse
from django.conf import settings
from .models import Order, OrderItem
from cart.cart import Cart

def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body)
    total_price = 0

    items = []

    for item in cart:
        product = item['product']
        total_price += round(product.get_formatted_discounted_price() * item['quantity'], 2)

        items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': product.get_formatted_discounted_price(),
            },
            'quantity': item['quantity']
        })


    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = items,
        mode = 'payment',
        success_url = 'http://127.0.0.1:8000/cart/success',
        cancel_url = 'http://127.0.0.1:8000/cart'
    )
    payment_intent = session.payment_intent

    order = Order.objects.create(
        user = request.user, 
        first_name = data['first_name'], 
        last_name = data['last_name'], 
        email = data['email'], 
        phone = data['phone'], 
        address = data['address'], 
        zipcode = data['zipcode'], 
        city = data['city'], 
        state = data['state'],
        payment_intent = payment_intent,
        paid = True,
        paid_amount = total_price,
    )

    for item in cart():
        product = item['product']
        quantity = int(item['quantity'])
        price = round(product.get_formatted_discounted_price() * quantity, 2)

        item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
    
    cart.clear()
    return JsonResponse({'session': session, 'order': payment_intent})