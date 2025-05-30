from django.shortcuts import render
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from myapp.forms import  UserInfoForm



def payment_success(request):
    return render(request, 'payment/payment_success.html')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if shipping_form.is_valid():
            shipping_form.save()
        context = {'cart_products': cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form}
        return render(request, 'payment/checkout.html', context)
    else:
        shipping_form = ShippingForm(request.POST or None)
        context = {'cart_products': cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form}
        return render(request, 'payment/checkout.html', context)
