from django.contrib import admin
from django.contrib.auth.models  import  Group
from .models import Product, ProductImage, Category, Brand, Material


admin.site.unregister(Group)

class ProductImageIstanceInline(admin.TabularInline):
    model = ProductImage
    min_num = 2
    max_num = 5
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'gender', 'size', 'color', 'footprint', 'green_points')
    inlines = [ProductImageIstanceInline]
    readonly_fields = ['footprint', 'green_points', 'slug']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'average_footprint')
    readonly_fields = ['average_footprint', 'slug']
    
admin.site.register(Brand)
admin.site.register(Material)
