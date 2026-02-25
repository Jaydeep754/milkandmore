from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='delivery_dashboard'),
    path('accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('order/<int:order_id>/', views.delivery_order_details, name='delivery_order_details'),
]