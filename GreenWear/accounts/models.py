from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    LEVELS = (
        ("1", "Consapevole Attivista"),
        ("2", "Guardiano dell'Ambiente"),
        ("3", "Ambasciatore Verde"),
        ("4", "Pilastro Ecologico"),
        ("5", "Spirito della Natura"),
    )
    
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        null=True, 
        blank=True
    )
    green_points = models.PositiveBigIntegerField(default=0)
    level = models.CharField(max_length=1, choices=LEVELS, default='1')
    
    def __str__(self):
        return self.username
