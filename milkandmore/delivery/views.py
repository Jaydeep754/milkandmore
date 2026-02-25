from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from orders.models import Order, DeliveryStatus
from accounts.models import DeliveryBoy
from django.db.models import Q
import json

@login_required
def dashboard(request):
    """Delivery person dashboard showing assigned and available orders"""
    if not request.user.is_delivery_boy:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get assigned orders
    assigned_orders = Order.objects.filter(
        delivery_boy=request.user,
        status__in=['out_for_delivery', 'confirmed']
    ).order_by('order_date')
    
    # Get available orders (pending and confirmed without delivery boy)
    available_orders = Order.objects.filter(
        Q(status='confirmed') | Q(status='pending'),
        delivery_boy__isnull=True
    ).order_by('order_date')
    
    # Get delivery history
    delivered_orders = Order.objects.filter(
        delivery_boy=request.user,
        status='delivered'
    ).order_by('-order_date')[:10]
    
    # Get delivery boy profile
    try:
        delivery_boy = DeliveryBoy.objects.get(user=request.user)
    except DeliveryBoy.DoesNotExist:
        delivery_boy = None
    
    context = {
        'assigned_orders': assigned_orders,
        'available_orders': available_orders,
        'delivered_orders': delivered_orders,
        'delivery_boy': delivery_boy
    }
    return render(request, 'delivery/dashboard.html', context)

@login_required
def accept_order(request, order_id):
    """Accept an order for delivery"""
    if not request.user.is_delivery_boy:
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, delivery_boy__isnull=True)
        
        order.delivery_boy = request.user
        order.status = 'out_for_delivery'
        order.save()
        
        DeliveryStatus.objects.create(
            order=order,
            status='out_for_delivery',
            updated_by=request.user,
            notes='Order accepted for delivery'
        )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
def update_order_status(request, order_id):
    """Update the status of an order being delivered"""
    if not request.user.is_delivery_boy:
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get('status')
        notes = data.get('notes', '')
        
        order = get_object_or_404(Order, id=order_id, delivery_boy=request.user)
        order.status = status
        order.save()
        
        DeliveryStatus.objects.create(
            order=order,
            status=status,
            updated_by=request.user,
            notes=notes
        )
        
        # Update delivery boy stats if order is delivered
        if status == 'delivered':
            try:
                delivery_boy = DeliveryBoy.objects.get(user=request.user)
                delivery_boy.total_deliveries += 1
                delivery_boy.save()
            except DeliveryBoy.DoesNotExist:
                pass
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
def delivery_order_details(request, order_id):
    """Get detailed information about an order for delivery person"""
    if not request.user.is_delivery_boy:
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
    order = get_object_or_404(Order, id=order_id)
    
    data = {
        'id': order.id,
        'customer_name': order.user.get_full_name() or order.user.username,
        'customer_phone': order.user.phone_number,
        'delivery_address': order.delivery_address,
        'delivery_time': order.delivery_time,
        'items': [
            {
                'name': item.product.name,
                'quantity': item.quantity,
                'price': float(item.price)
            } for item in order.items.all()
        ],
        'total': float(order.total_amount)
    }
    
    return JsonResponse(data)