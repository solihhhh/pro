from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.cart_view, name='cart_view'),
    path('liked-products/', views.liked_products, name='liked_products'),
    path('like-product/<int:product_id>/', views.like_product, name='like_product'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/like/', views.like_product, name='like_product'),
    path('product/<int:product_id>/comment/', views.add_comment, name='add_comment'),
    path('product/<int:product_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
]
