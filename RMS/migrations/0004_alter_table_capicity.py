# Generated by Django 3.2 on 2021-05-26 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RMS', '0003_alter_booking_capicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='capicity',
            field=models.PositiveIntegerField(),
        ),
    ]
