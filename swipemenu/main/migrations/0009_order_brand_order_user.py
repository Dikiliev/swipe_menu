# Generated by Django 5.0 on 2023-12-28 20:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='main.brand', verbose_name='Бренд'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
    ]
