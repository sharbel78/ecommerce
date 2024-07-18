from django.shortcuts import render, redirect, get_object_or_404
from shopApp.models import product
from .models import  Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _cart_id(request):
    cart1=request.session.session_key
    if not cart1:
        cart1=request.session.create()
    return cart1
def add_cart(request,product_id):
    product1 = product.objects.get(id=product_id)
    try:
        Cart1 = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        Cart1=Cart.objects.create(cart_id=_cart_id(request))
        Cart1.save()
    try:
        cart_item = CartItem.objects.get(product1=product1,Cart1=Cart1)
        if cart_item.quantity < cart_item.product1.stock:
            cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
                product1=product1,
                quantity=1,
                Cart1=Cart1,
        )
        cart_item.save()
    return redirect('cart:cart_detail')
def cart_detail(request,total=0,counter=0,cart_item=None):
    try:
        Cart1=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(Cart1=Cart1,active=True)
        for cart_item in cart_items:
            total+=(cart_item.product1.price * cart_item.quantity)
            counter+= cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return  render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))


def cart_remove(request,product_id):
    Cart1=Cart.objects.get(cart_id=_cart_id(request))
    product1=get_object_or_404(product,id=product_id)
    cart_item=CartItem.objects.get(product1=product1,Cart1=Cart1)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')
def full_remove(request,product_id):
    Cart1 = Cart.objects.get(cart_id=_cart_id(request))
    product1 = get_object_or_404(product, id=product_id)
    cart_item = CartItem.objects.get(product1=product1, Cart1=Cart1)
    cart_item.delete()
    return redirect('cart:cart_detail')

