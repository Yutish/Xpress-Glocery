# Generated by Django 3.0.8 on 2020-10-18 15:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0028_order_received'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order_Received',
            new_name='Received_Order',
        ),
    ]
