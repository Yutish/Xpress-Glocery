# Generated by Django 3.0.8 on 2020-08-09 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20200809_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='desc',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
    ]
