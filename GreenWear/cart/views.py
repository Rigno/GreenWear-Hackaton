from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cart
from products.models import Product
from accounts.models import Discount


# --- CART --- #
@login_required(login_url='login')
def cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.products.all()
    
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
            messages.info(request, "Il codice sconto non è valido")

    else:
        discount = 0
        cart_total = cart.get_total()

    context = {
        'cart': cart,
        'products': cart_items,
        'cart_total': cart_total,
        'discount': discount,
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
        for product in [item.product for item in cart_items]:
            points += product.green_points
            
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
        
        return redirect('home')
    
    else:
        messages.info(request, "Il carrello è vuoto, aggiungi delgi articoli prima di continuare")
        return redirect('cart')