# Generated by Django 3.0.8 on 2020-10-18 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_received_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='received_order',
            name='total_amount',
            field=models.FloatField(),
        ),
    ]
