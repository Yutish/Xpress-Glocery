# Generated by Django 3.0.8 on 2020-08-11 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='short-product-name'),
            preserve_default=False,
        ),
    ]