# Generated by Django 3.2 on 2021-05-26 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RMS', '0005_rename_food_booking_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='On_Off',
            field=models.BooleanField(null=True),
        ),
    ]