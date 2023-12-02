from django.db import models
from accounts.models import CustomUser
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    
    def add_to_cart(self, product, quantity):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        cart_item.quantity += quantity
        cart_item.save()

    def remove_from_cart(self, product):
        CartItem.objects.filter(cart=self, product=product).delete()
        
    def get_total_items(self):
        return sum(cart_item.quantity for cart_item in self.cartitem_set.all())
    
    def get_total(self, discount_code=''):
        cart_items = self.cartitem_set.all()
        total = 0
        for item in cart_items:
            if item.product.discounted_price:
                total += item.product.discounted_price * item.quantity
            else:
                total += item.product.price * item.quantity
                
        if discount_code in [discount.code for discount in self.user.discounts.all()]:
            save = self.user.discounts.get(code=discount_code).saving
            total -= save
        
        return total if total >= 0 else 0     


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
