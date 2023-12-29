import datetime
import random

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
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

    def get_brand(self):
        return Brand.objects.get(user_id=self.id)

    def get_avatar_url(self):
        if not self.avatar:
            return 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png'

        return self.avatar.url


class Brand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='brands')

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

    def get_product_5(self):
        return Product.objects.filter(brand_id=self.id)[:5]

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

    def get_price(self):
        return int(self.price)

    def get_custom_dict(self):
        res = {
            'title': self.title,
        }

        return res


class Order(models.Model):
    ORDER_TYPE_CHOICES = (
        (1, 'На вынос'),
        (2, 'В заведении'),
        (3, 'С доставкой'),
    )

    ORDER_STATUS_CHOICES = (
        (1, 'Принято'),
        (2, 'В процессе'),
        (3, 'Готово'),
        (4, 'Завершен'),
    )

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд', related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='orders')

    order_number = models.PositiveIntegerField(unique=True,
                                               validators=[MinValueValidator(10000),MaxValueValidator(99999),],
                                               verbose_name='Номер заказа')

    order_type = models.IntegerField(default=1, choices=ORDER_TYPE_CHOICES, verbose_name='Тип заказа')
    order_status = models.IntegerField(default=1, choices=ORDER_STATUS_CHOICES, verbose_name='Статус')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ №{self.order_number} ({self.get_order_type_display()}) - {self.get_order_status_display()}"

    def generate_order_number(self):
        while True:
            order_number = random.randint(10000, 99999)
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def get_sum(self):
        total = 0
        items = OrderItem.objects.filter(order_id=self.id)
        for item in items:
            total += item.quantity * item.product.price

        return total

    def get_type(self):
        for num, name in self.ORDER_TYPE_CHOICES:
            if num == self.order_type:
                return name

    def get_created_date(self):
        formatted_date = self.created_at.strftime('%d.%m.%Y %H:%M')
        return formatted_date


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def sum(self):
        return int(self.product.price * self.quantity)

    def __str__(self):
        return f"{self.product.title} x{self.quantity}"
