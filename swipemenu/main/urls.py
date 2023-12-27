from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-brand/', views.create_brand, name='create-brand'),
    path('brand/', views.brand, name='brand'),
    path('add-product/', views.add_product, name='add-product'),
    path('catalog/', views.catalog, name='catalog'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
