# Generated by Django 3.2 on 2021-06-01 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RMS', '0014_alter_contactus_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='check_sum',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
