# Generated by Django 4.2.7 on 2023-12-02 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='quiz_lives',
            field=models.PositiveIntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='green_points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
