from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_ENUM = (
        (1, 'Покупатель'),
        (2, 'Владелец заведения'),
    )

    role = models.IntegerField(
        choices=ROLE_ENUM,
        default=1
    )

    avatar = models.ImageField(blank=True, verbose_name='Аватарка')
    phone_number = models.CharField(max_length=25, blank=True, verbose_name='Номер телефона')
    address = models.CharField(max_length=150, blank=True, verbose_name='Адрес')

    def __str__(self):
        return self.username

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def exist(self):
        return len(User.objects.filter(username=self.username)) > 0

    def have_brand(self):
        return len(Brand.objects.filter(user_id=self.id)) > 0


class Brand(models.Model):
    user_id = models.IntegerField()

    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    address = models.CharField(max_length=150, verbose_name='Адрес')
    phone_number = models.CharField(max_length=25, blank=True, verbose_name='Номер телефона')
    avatar = models.ImageField(blank=True, verbose_name='Аватарка')

    def __str__(self):
        return self.title

    def get_title(self):
        return self.title

    def get_product(self):
        return Product.objects.filter(brand_id=self.id)

    def exist(self):
        return len(User.objects.filter(username=self.title)) > 0


class Product(models.Model):
    brand_id = models.IntegerField()

    title = models.CharField(max_length=255, verbose_name='Название')
    composition = models.TextField(blank=True, verbose_name='Состав')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='product_images/', verbose_name='Картинка')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title
