from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.contrib import messages
from myapp.models import Product
from django.http import JsonResponse


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    context = {'cart_products': cart_products, 'quantities':quantities, 'totals':totals}
    return render(request, 'cart/cart_summary.html', context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()
        # response = JsonResponse({'Product Name': product.name})
        # return response
        response = JsonResponse({'qty': cart_quantity})
        messages.error(request, " Product Added TO Cart...... ")

        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        # call delete function in cart
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.error(request, " Item Deleted From Shopping Cart...... ")
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') =='post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.error(request, " Your Cart Has Been Updated...... ")
        return response
        # return redirect('cart_summar/y')
