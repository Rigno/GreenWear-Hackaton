from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Product, Category

@receiver(post_save, sender=Product)
def update_average_footprint(sender, instance, created, **kwargs):
    pass
