# Generated by Django 5.0 on 2023-12-27 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_user_address_alter_brand_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'Покупатель'), (2, 'Владелец заведения')], default=1),
        ),
    ]
