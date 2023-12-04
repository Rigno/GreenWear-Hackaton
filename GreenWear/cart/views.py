from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests

from cart.models import Cart
from products.models import Product
from accounts.models import Discount
from core.models import FACTORY_LOCATION


# --- CART --- #
@login_required(login_url='login')
def cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.products.all()
    user_location = user.location
    
    # calculate shipping footprint:
    url = 'http://194.233.164.36/api/calculateCO2'
    headers = {
        'x-tenant': 'greenwear',
        'x-apikey': 'XNwtvpHY6skocyd+0B+I1w4p51oWdxXEjREEpa9LPcE=',
    }

    payload = {
        "transport": {
            "shippingFrom": "{0};{1}".format(FACTORY_LOCATION[0], FACTORY_LOCATION[1]),
            "shippingTo": user_location
        },
        "production": [
        {
            "materialLocation": "0;0",
            "factoryLocation": "0;0",
            "weight": 1,
            "material": "metallo"
        }
        ]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    shipping_footprint = data['transportCO2']
    
    # handel cart total and discount codes:
    if request.method == 'GET':
        code = request.GET.get('codice_sconto')
        discount = 0
        cart_total = cart.get_total()
        
        if user.green_points >= 1000:
            code10, created = Discount.objects.get_or_create(code='GREENWEAR1000', saving=10)
            user = user
            user.discounts.add(code10)
            user.save()
            is_applicable = True 
        else:
            request.session['discount'] = "not_valid"
            is_applicable = False

        if code in [discount.code for discount in user.discounts.all()]:
            if cart.get_total() < 50:
                messages.info(request, "Il codice è applicabile solo su una spesa superiore a €50")
                return redirect('cart')
            elif not is_applicable:
                messages.info(request, "Per applicare il codice devi avere almeno 1000 punti green")
                return redirect('cart')
            discount = user.discounts.get(code=code).saving
            cart_total = cart.get_total(discount_code=code)
            request.session['discount'] = "is_valid"
        elif code:
            request.session['discount'] = "not_valid"
            messages.info(request, "Il codice sconto non è valido")

    else:
        discount = 0
        cart_total = cart.get_total()

    context = {
        'cart': cart,
        'products': cart_items,
        'cart_total': cart_total,
        'discount': discount,
        'shipping_footprint': shipping_footprint,
    }
    return render(request, 'cart/cart.html', context)

# --- MODIFY ITEM QUANTITY --- #
def modify_item_quantity(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        quantity = request.POST.get('quantità')

        if quantity:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item = cart.cartitem_set.get(product=product)
            cart_item.quantity = quantity
            cart_item.save()

            return redirect('cart')
        
        else:
            return redirect('cart')
    else:
        return redirect('cart')

# --- REMOVE ITEM --- #
def remove_item(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.remove_from_cart(product=product)
    
    return redirect('cart')

# --- CHECKOUT --- #
def checkout(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = cart.cartitem_set.all()
    
    if len(cart_items) > 0:
        points = 0
        for i in [item for item in cart_items]:
            points += (i.product.green_points * i.quantity)
            
        cart.delete()
        
        print(request.session.get('discount', None))
        
        if request.session.get('discount', None) == 'is_valid':
            user.green_points -= 1000            
        
        user.green_points += points
        user.save()
        
        if points:
            messages.info(request, "L'acquisto è stato completato con successo, hai guadagnato +{0} punti!".format(points))
        else:
            messages.info(request, "L'acquisto è stato completato con successo")
        
        return redirect('shop')
    
    else:
        messages.info(request, "Il carrello è vuoto, aggiungi delgi articoli prima di continuare")
        return redirect('cart')