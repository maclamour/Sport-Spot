# Generated by Django 4.1.2 on 2022-10-11 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_product_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(default='', upload_to='main_app/images'),
        ),
    ]
