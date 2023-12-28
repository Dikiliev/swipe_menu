from django.http import HttpRequest
from .models import User, Brand, Product


def get_product(request: HttpRequest, product_id: int):
    print(request.method)

    result = Product.objects.filter(id=product_id)

    if result is None:
        return {}

    return Response(serializer.data)
