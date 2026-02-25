from django.urls import path
from . import views

urlpatterns = [
    # 👉 SPECIFIC URLs FIRST (order matters!)
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('debug-cart/', views.debug_cart, name='debug_cart'),  # Add this line
    
    # 👉 GENERIC URL LAST (catches everything else)
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    
    # 👉 Empty path should be first or last? Actually first is fine
    path('', views.product_list, name='product_list'),
]