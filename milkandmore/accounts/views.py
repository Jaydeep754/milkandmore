from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Customer, DeliveryBoy
from products.models import Product

def register_choice(request):
    return render(request, 'accounts/register_choice.html')

def register_customer(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone,
            address=address,
            is_customer=True
        )
        
        # Create customer profile
        Customer.objects.create(user=user)
        
        # Log the user in
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('home')
    
    return render(request, 'accounts/register_customer.html')

def register_delivery(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        vehicle = request.POST['vehicle_number']
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone,
            is_delivery_boy=True
        )
        
        # Create delivery boy profile
        DeliveryBoy.objects.create(user=user, vehicle_number=vehicle)
        
        messages.success(request, 'Delivery partner registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'accounts/register_delivery.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user type
            if user.is_delivery_boy:
                return redirect('delivery_dashboard')
            elif user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    
    if user.is_customer:
        customer = Customer.objects.get(user=user)
        orders = user.order_set.all().order_by('-order_date')[:5]
        context['customer'] = customer
        context['orders'] = orders
    
    return render(request, 'accounts/profile.html', context)