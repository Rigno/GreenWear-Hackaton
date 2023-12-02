from django.contrib import admin
from django.contrib.auth.models  import  Group
from .models import Product, ProductImage, Category, Brand, Material, Size, Color


admin.site.unregister(Group)

# Save all objects
@admin.action(description='Save objects')
def save_objects(modeladmin, request, queryset):
    for obj in queryset:
        obj.save()

admin.site.add_action(save_objects)


class ProductImageIstanceInline(admin.TabularInline):
    model = ProductImage        

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'gender', 'footprint', 'green_points')
    inlines = [ProductImageIstanceInline]
    readonly_fields = ['footprint', 'green_points', 'slug']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'average_footprint')
    readonly_fields = ['average_footprint', 'slug']
    
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Material)
