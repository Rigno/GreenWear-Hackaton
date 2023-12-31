# Generated by Django 4.2.7 on 2023-11-28 15:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_material_remove_product_material_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='latitude',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)]),
        ),
        migrations.AddField(
            model_name='material',
            name='longitude',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
        ),
    ]
