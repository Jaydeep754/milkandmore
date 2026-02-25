from django.urls import path
from . import views

urlpatterns = [
    path('register/choice/', views.register_choice, name='register_choice'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/delivery/', views.register_delivery, name='register_delivery'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]