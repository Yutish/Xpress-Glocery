# Generated by Django 3.0.8 on 2020-08-25 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_auto_20200825_2238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='item',
            new_name='product',
        ),
    ]
