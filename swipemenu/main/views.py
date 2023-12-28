import json

from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import User, Brand, Product, Order, OrderItem

DEFAULT_TITLE = 'DjangoDev'


def home(request: HttpRequest):
    data = create_base_data()
    return render(request, 'index.html', data)


def create_brand(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.have_brand():
        return redirect('brand')

    data = create_base_data('Создание заведения')

    def get():
        return render(request, 'create_brand.html', data)

    def post():
        post = request.POST

        brand = Brand()
        brand.user_id = request.user.id
        brand.title = post.get('username', '')
        brand.description = post.get('description', '')
        brand.address = post.get('address', '')
        brand.phone_number = post.get('phone_number', '')

        uploaded_image = request.FILES.get('image_file', None)

        brand.avatar.save(uploaded_image.name, uploaded_image)

        brand.save()

        return redirect('home')

    if request.method == 'POST':
        return post()
    return get()


def brand(request: HttpRequest, brand_id: int):
    data = create_base_data('Заказ')
    data['brand'] = Brand.objects.filter(id=brand_id)[0]
    return render(request, 'brand.html', data)


def edit_brand(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.have_brand():
        return redirect('create-brand')

    data = create_base_data('Мое заведения')
    data['brand'] = Brand.objects.filter(user_id=request.user.id)[0]
    return render(request, 'edit_brand.html', data)


def add_product(request: HttpRequest):
    data = create_base_data('Добавление товара')

    def get():
        return render(request, 'create_product.html', data)

    def post():
        post = request.POST

        product = Product()

        product.brand_id = Brand.objects.get(user_id=request.user.id).id
        product.title = post.get('username', '')
        product.composition = post.get('composition', '')
        product.description = post.get('description', '')
        product.price = post.get('price', 0)

        uploaded_image = request.FILES.get('image_file', None)

        product.image.save(uploaded_image.name, uploaded_image)

        product.save()

        return redirect('edit-brand')

    if request.method == 'POST':
        return post()
    return get()


@csrf_exempt
def order(request: HttpRequest, order_id: int):
    data = create_base_data(f'Заказ {order_id}')

    if request.method == "POST":
        data = json.loads(request.body)
        products = data['products']

        user = User.objects.get(id=data['user_id'])
        brand = Brand.objects.get(id=data['brand_id'])

        order = Order.objects.create(user=user, brand=brand)

        order_items = []
        for product in products:
            product_db = Product.objects.get(id=int(product['id']))
            order_item = OrderItem.objects.create(order=order, product=product_db, quantity=product['count'])
            order_items.append(order_item)

        order.save()

        for order_item in order_items:
            order_item.save()

        response_data = {"message": "Данные успешно получены", 'data': products}
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Метод запроса должен быть POST"})


def user_orders(request: HttpRequest):
    pass


def catalog(request: HttpRequest):
    data = create_base_data('Каталог')
    data['brands'] = []

    brands = Brand.objects.all()
    data['brands'] = brands

    print(data)

    return render(request, 'catalog.html', data)


def register(request: HttpRequest):
    data = create_base_data('Регистрация')

    def get():
        return render(request, 'registration/register.html', data)

    def post():
        post_data = request.POST

        user = User()
        user.username = post_data.get('username', '')
        user.email = post_data.get('email', '')

        password = post_data.get('password', '')

        data['username'] = user.username
        data['email'] = user.email

        def check_validate():
            if len(user.username) < 3:
                data['error'] = '* Имя пользователся должно состоять как минимум из 3 симьволов'
                return False

            if user.exist():
                data['error'] = '* Такой пользователь уже существует'
                return False

            if len(password) < 8:
                data['error'] = '* Пароль должен состоять как минимум из 8 симьволов'
                return False
            return True

        if not check_validate():
            return render(request, 'registration/register.html', data)

        user.set_password(password)
        user.save()
        login(request, user)

        return redirect('home')

    if request.method == 'POST':
        return post()
    return get()


def user_login(request: HttpRequest):
    data = create_base_data('Вход')

    def get():
        return render(request, 'registration/login.html')

    def post():
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return redirect('home')

        data['error'] = '* Неверное имя пользователя или пароль'
        return render(request, 'registration/login.html', data)

    if request.method == 'POST':
        return post()
    return get()


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('login')


# Help functions
def create_base_data(title: str = None):
    if not title:
        title = DEFAULT_TITLE

    return {
        'title': title,
    }
