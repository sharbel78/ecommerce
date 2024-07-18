from .models import Cart,CartItem
from .views import _cart_id

def counter(request):
    item_counter=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            Cart1=Cart.objects.filter(cart_id=_cart_id(request))
            car_items=CartItem.objects.all().filter(Cart1=Cart1[:1])
            for cart_items in car_items:
                item_counter += cart_items.quantity
        except Cart.DoesNotExist:
            item_counter = 0
    return  dict(item_counter=item_counter)