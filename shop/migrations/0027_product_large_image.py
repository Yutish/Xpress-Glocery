# Generated by Django 3.0.8 on 2020-10-18 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_auto_20201018_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='large_image',
            field=models.ImageField(default='', upload_to='shop/images'),
        ),
    ]
