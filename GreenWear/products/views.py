from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from products.models import Product, Size, Color
from cart.models import Cart, CartItem


# --- PRODUCT DETAIL --- #
def product(request, slug):
    product_detail = get_object_or_404(Product, slug=slug)
    other_products = Product.objects.order_by('?').exclude(slug=product_detail.slug)[0:3]
    sizes = Size.objects.all()
    colors = Color.objects.all()

    context = {
        'product': product_detail,
        'other_products': other_products,
        'sizes': sizes,
        'colors': colors,
    }
    return render(request, 'products/product.html', context)

# --- ADD TO CART --- #
@login_required(login_url='login')
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        size = request.POST.get('taglia')
        color = request.POST.get('colore')
        quantity = int(request.POST.get('quantità'))

        if size and color and quantity:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart.add_to_cart(product=product, quantity=quantity)

            return redirect('cart')
        
        else:
            return redirect('product', slug)
    else:
        return redirect('product', slug)
