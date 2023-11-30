# Generated by Django 4.2.7 on 2023-11-29 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_product_materials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='materials',
            field=models.ManyToManyField(blank=True, related_name='materials', to='products.material'),
        ),
    ]