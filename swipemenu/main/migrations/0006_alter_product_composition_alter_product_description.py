# Generated by Django 5.0 on 2023-12-27 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_product_images_product_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='composition',
            field=models.TextField(blank=True, verbose_name='Состав'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
