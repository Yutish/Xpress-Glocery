# Generated by Django 3.0.8 on 2020-10-18 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20201018_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_request',
            name='time',
            field=models.TimeField(default=None),
        ),
    ]
