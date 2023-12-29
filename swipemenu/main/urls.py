from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.home, name='home'),
    path('create-brand/', views.create_brand, name='create-brand'),
    path('brand/<int:brand_id>/', views.brand, name='brand'),
    path('edit-brand/', views.edit_brand, name='edit-brand'),
    path('add-product/', views.add_product, name='add-product'),

    path('catalog/', views.catalog, name='catalog'),
    path('shorts/', views.show_shorts, name='shorts'),
    path('get-short/', views.get_short, name='get-short'),

    path('get-user/<int:user_id>', views.get_user, name='get-user'),

    path('add-comment/', views.add_comment, name='add-comment'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('add-order/', views.add_order, name='add-order'),
    path('orders-for-user/', views.user_orders, name='orders-for-user'),
    path('orders-for-owner/', views.owner_orders, name='orders-for-owner'),

    path('set-order-status/', views.set_order_status, name='set-order-status'),

    path('api/get-product/<int:product_id>/', api.get_product, name='get-product'),
]
