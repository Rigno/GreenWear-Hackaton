# Generated by Django 4.2.7 on 2023-12-03 17:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_product_users_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='weight',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]