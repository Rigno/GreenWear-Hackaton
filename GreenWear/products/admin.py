from django.contrib import admin
from django.contrib.auth.models  import  Group
from .models import Product, ProductImage, Category, Brand, Material, Size, Color, Location


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
    
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'location')
    
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    
admin.site.register(Brand)
admin.site.register(Size)
