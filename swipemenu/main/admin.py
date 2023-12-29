from django.contrib import admin
from .models import User, Brand, Product, Order, OrderItem, Short

admin.site.register(User)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Short)
