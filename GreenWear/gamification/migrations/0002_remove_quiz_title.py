# Generated by Django 4.2.7 on 2023-12-02 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='title',
        ),
    ]
