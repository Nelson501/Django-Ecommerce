from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, Order_items
from django.contrib.auth.models import User
from django.contrib import messages
from myapp.models import Product



def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        context = {'orders':orders}
        return render(request, "payment/shipped_dash.html", context)
    else:
        messages.success(request, 'Access Denied!')
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        context = {'orders':orders}
        return render(request, "payment/not_shipped_dash.html", context)
    else:
        messages.success(request, 'Access Denied!')
        return redirect('home')
    


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        payment_form = PaymentForm(request.POST or None)
        # get shipping sessions
        my_shipping = request.session.get('my_shipping')
        # print(my_shipping)

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']


        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        # print(shipping_address)
        amount_paid = totals
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # add items order
            order_id = create_order.pk

            for product in cart_products:
                product_id = product.id
                if product.sale:
                    price = product.sale_price
                else:
                    price = product.price


                for key, value in quantities.items():
                    if  int(key) == product.id:
                        # create order item
                        create_order_item = Order_items(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
                    
            messages.success(request, 'Order placed!')
            return redirect('home')
            
        else:
            # not logged in 

            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            order_id = create_order.pk

            for product in cart_products:
                product_id = product.id
                if product.sale:
                    price = product.sale_price
                else:
                    price = product.price


                for key, value in quantities.items():
                    if  int(key) == product.id:
                        # create order item
                        create_order_item = Order_items(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, 'Order placed!')
            return redirect('home')
    else:
        messages.error(request, 'Access DEnied')
        return redirect('home')






def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            context = {'cart_products': cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form}
            return render(request, 'payment/billing_info.html', context)
        else:
            billing_form = PaymentForm()
            context = {'cart_products': cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form':billing_form}
            return render(request, 'payment/billing_info.html', context)
    else:
        messages.error(request, 'Access Denied')
        return redirect('home')

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




def payment_success(request):
    
    return render(request, 'payment/payment_success.html')
