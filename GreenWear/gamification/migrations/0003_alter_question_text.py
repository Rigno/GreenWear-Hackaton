# Generated by Django 4.2.7 on 2023-12-02 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0002_remove_quiz_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(max_length=255),
        ),
    ]
