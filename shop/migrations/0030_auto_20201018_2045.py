# Generated by Django 3.0.8 on 2020-10-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_auto_20201018_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='received_order',
            name='items',
        ),
        migrations.AddField(
            model_name='received_order',
            name='items',
            field=models.TextField(default=None),
        ),
    ]
