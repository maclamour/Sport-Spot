# Generated by Django 4.1.2 on 2023-10-05 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_rename_items_cart_order_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='order_items',
            new_name='items',
        ),
    ]