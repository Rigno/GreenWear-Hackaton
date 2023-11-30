from products.models import Category, Product
from cart.models import Cart

def custom_context(request):
    if request.user.is_authenticated:
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        total_items = user_cart.get_total_items()
        wishlist_products = Product.objects.filter(users_wishlist=request.user)
    else:
        total_items = None
        wishlist_products = None

    return {
        'categories': Category.objects.all(),
        'cart_items': total_items,
        'wishlist_products': wishlist_products,
    }
