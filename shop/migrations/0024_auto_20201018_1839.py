# Generated by Django 3.0.8 on 2020-10-18 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20201018_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_request',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
