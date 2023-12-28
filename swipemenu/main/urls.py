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
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('order/<int:order_id>/', views.order, name='order'),

    path('api/get-product/<int:product_id>/', api.get_product, name='get-product'),
]
