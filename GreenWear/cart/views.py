from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Cart


# --- CART --- #
@login_required(login_url='login')
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.products.all()
    
    context = {
        'cart': cart,
        'products': cart_items
    }
    return render(request, 'cart/cart.html', context)
