from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

from products.models import Product


# --- LOGIN --- #
def login(request):
    
    context = {
        
    }
    return render(request, 'accounts/login.html', context)

# --- SIGNUP --- #
def signup(request):
    
    context = {
        
    }
    return render(request, 'accounts/signup.html', context)

# --- WISHLIST --- #
@login_required(login_url='login')
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    
    context = {
        'wishlist_products': products,
    }
    return render(request, 'accounts/wishlist.html', context)

@login_required(login_url='login')
def modify_wishlist(request):

    if request.method == 'POST':
        product_name = request.POST.get('name')
        print(product_name)
        product = get_object_or_404(Product, name=product_name)
        print(product)
        
        if product.users_wishlist.filter(id=request.user.id).exists():
            product.users_wishlist.remove(request.user)
            data = {'is_present': False}
        else:
            product.users_wishlist.add(request.user)
            data = {'is_present': True}

        return JsonResponse(data)

# --- ACCOUNT --- #
@login_required(login_url='login')
def account(request):
    
    context = {
        
    }
    return render(request, 'accounts/account.html', context)