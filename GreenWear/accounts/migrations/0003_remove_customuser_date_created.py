# Generated by Django 4.2.7 on 2023-11-26 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customuser_name_remove_customuser_surname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='date_created',
        ),
    ]