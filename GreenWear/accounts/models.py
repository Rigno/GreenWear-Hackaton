from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator


NUM_LIVES = 5

class Discount(models.Model):
    code = models.CharField(max_length=20)
    saving = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "discount code"
        verbose_name_plural = "discount codes"
        

class CustomUser(AbstractUser):
    LEVELS = (
        ("1", "Consapevole Attivista"),
        ("2", "Guardiano dell'Ambiente"),
        ("3", "Ambasciatore Verde"),
        ("4", "Pilastro Ecologico"),
        ("5", "Spirito della Natura"),
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        null=True, 
        blank=True
    )
    green_points = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=1, choices=LEVELS, default='1')
    quiz_lives = models.PositiveIntegerField(default=NUM_LIVES, validators=[MaxValueValidator(NUM_LIVES)])
    discounts = models.ManyToManyField(Discount, blank=True)
    
    def __str__(self):
        return self.username
