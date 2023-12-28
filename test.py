class Order(models.Model):
    TYPE_ENUM = (
        (1, 'На вынос'),
        (2, 'В заведении'),
        (3, 'С доставкой'),
    )

    STATUS_ENUM = (
        (1, 'Принято'),
        (2, 'В процессе'),
        (3, 'Готово'),
    )

    order_number = models.PositiveIntegerField(unique=True, null=False, blank=False, editable=False)
    items = models.ManyToManyField(Product, through='OrderItem', related_name='orders', blank=True)

    type = models.IntegerField(choices=TYPE_ENUM, default=1)
    status = models.IntegerField(choices=TYPE_ENUM, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} ({self.created_at})"

    def generate_order_number(self):
        while True:
            order_number = random.randint(1000, 9999)
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')

    def __str__(self):
        return f"{self.product.name} {self.quantity}шт"