# Generated by Django 4.1.2 on 2023-10-05 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_product_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='complated_order',
            new_name='completed_order',
        ),
    ]
