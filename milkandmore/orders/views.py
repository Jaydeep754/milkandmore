from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Order, OrderItem, DeliveryStatus, Cart
from products.models import Product
from accounts.models import DeliveryBoy
import json

@login_required
def checkout(request):
    """Checkout page - shows order summary and collects delivery info"""
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    items = cart.items.all()
    
    if not items:
        messages.error(request, 'Your cart is empty!')
        return redirect('product_list')
    
    total = sum(item.product.price * item.quantity for item in items)
    
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', request.user.address)
        delivery_time = request.POST.get('delivery_time')
        payment_method = request.POST.get('payment_method', 'cod')
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            delivery_address=delivery_address,
            delivery_time=delivery_time,
            payment_method=payment_method
        )
        
        # Create order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            
            # Update stock
            product = item.product
            product.stock -= item.quantity
            product.save()
        
        # Create initial status
        DeliveryStatus.objects.create(
            order=order,
            status='pending',
            updated_by=request.user,
            notes='Order placed successfully'
        )
        
        # Clear cart
        cart.is_active = False
        cart.save()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'cart': cart,
        'items': items,
        'total': total,
        'user': request.user
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_history(request):
    """Display user's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    context = {'orders': orders}
    return render(request, 'orders/history.html', context)

@login_required
def order_detail(request, order_id):
    """Show details of a specific order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'orders/detail.html', context)

@login_required
def cancel_order(request, order_id):
    """Cancel an order if it's still pending"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()
        
        # Restore stock
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        
        DeliveryStatus.objects.create(
            order=order,
            status='cancelled',
            updated_by=request.user,
            notes='Order cancelled by customer'
        )
        
        messages.success(request, 'Order cancelled successfully.')
    else:
        messages.error(request, 'Order cannot be cancelled at this stage.')
    
    return redirect('order_detail', order_id=order.id)