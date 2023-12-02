from django.db import models, transaction
from accounts.models import CustomUser
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

from .utils import calculate_footprints


class Category(models.Model):   
    name = models.CharField(max_length=50)
    average_footprint = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    slug = models.SlugField(max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        
        products = Product.objects.filter(category__name=self.name)
        total_footprint = sum([product.footprint for product in products])
        self.average_footprint = total_footprint / len(products) if len(products) > 0 else 0

        super(Category, self).save(*args, **kwargs)
        
    def get_products(self):
        return Product.objects.filter(category__name=self.name)
        
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        
        
class Material(models.Model):   
    name = models.CharField(max_length=50)
    weight = models.PositiveIntegerField(default=1)
    latitude = models.FloatField(blank=True, null=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(blank=True, null=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "material"
        verbose_name_plural = "materials"

        

class Brand(models.Model):   
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "brand"
        verbose_name_plural = "brands"
 
        
class Color(models.Model):   
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7, help_text="Insert the hex code for the color")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "color"
        verbose_name_plural = "colors"

    
class Size(models.Model):   
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "size"
        verbose_name_plural = "sizes"


class Product(models.Model):
    GENDERS = (
        ('M', 'Uomo'),
        ('F', 'Donna'),
        ('U', 'Unisex'),
    )
    
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name="brand")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    description = models.TextField(max_length=500, default='')
    gender = models.CharField(max_length=1, choices=GENDERS)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sizes = models.ManyToManyField(Size, related_name="size")
    colors = models.ManyToManyField(Color, related_name="color")
    materials = models.ManyToManyField(Material, related_name="materials")
    footprint = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    green_points = models.PositiveIntegerField(null=True, blank=True)
    users_wishlist = models.ManyToManyField(CustomUser, related_name="wishlist", blank=True)
    data = models.DateField(auto_now_add=True, editable=False)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
        transaction.on_commit(lambda: self.auto_complete())
        
    def auto_complete(self, *args, **kwargs):
        self.footprint = calculate_footprints(self.materials.all())
        avg = float(self.category.average_footprint)
        
        if self.footprint < avg*0.5:
            self.green_points = 10
        elif self.footprint < avg*0.75:
            self.green_points = 20
        elif self.footprint < avg*0.9:
            self.green_points = 30
        else:
            self.green_points = 0
            
        super(Product, self).save(*args, **kwargs)
        self.category.save()

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"


def product_image_path(instance, filename):
    return f'product_images/{instance.product.name}/{filename}'
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name="product_images")
    image = models.ImageField(upload_to=product_image_path)
    is_feature = models.BooleanField(default=False)
