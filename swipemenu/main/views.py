from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest
from django.shortcuts import render, redirect

from .models import User, Brand, Product

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


def brand(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user.have_brand():
        return redirect('create-brand')

    data = create_base_data('Мое заведения')
    return render(request, 'brand.html', data)


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

        return redirect('home')

    if request.method == 'POST':
        return post()
    return get()


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
