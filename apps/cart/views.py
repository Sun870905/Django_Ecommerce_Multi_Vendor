import stripe
from config.settings.production import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps.orders.utils import checkout, notify_customer, notify_vendor

from .cart import Cart
from .forms import CheckoutForm


def cart_detail(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            stripe.api_key = STRIPE_SECRET_KEY
            stripe_token = form.cleaned_data['stripe_token']
            try:
                charge = stripe.Charge.create(
                    amount=int(cart.get_total_cost() * 100),
                    currency='USD',
                    description='Charge from E-commerce',
                    source=stripe_token
                )
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                place = form.cleaned_data['place']
                order = checkout(
                    request,
                    first_name,
                    last_name,
                    email,
                    address,
                    zipcode,
                    place,
                    phone,
                    cart.get_total_cost()
                )
                cart.clear()
                notify_customer(order)
                notify_vendor(order)
                return redirect('success')
            except Exception:
                messages.error(
                    request,
                    'There was something wrong with the payment.'
                )
    else:
        form = CheckoutForm()
    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)
    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')
    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart')
    context = {'form': form, 'stripe_public_key': STRIPE_PUBLIC_KEY}
    return render(request, 'cart/cart.html', context)


class Success(TemplateView):
    template_name = "cart/messages/success.html"
