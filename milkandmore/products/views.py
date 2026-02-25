from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from orders.models import Cart
import json

# ✅ ADD THIS HOME FUNCTION FIRST
def home(request):
    """Home page view"""
    categories = Category.objects.filter(parent__isnull=True)[:6]  # Show main categories
    featured_products = Product.objects.filter(available=True)[:8]  # Show 8 featured products
    
    # Get cart count if user is logged in
    cart_count = 0
    if request.user.is_authenticated:
        from orders.models import Cart
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        cart_count = cart.items.count()
    
    # Debug print (check console)
    print(f"Homepage loading: {featured_products.count()} products found")
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'cart_count': cart_count
    }
    return render(request, 'index.html', context)

# ✅ THEN THE REST OF YOUR VIEW FUNCTIONS
def product_list(request):
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, available=True)
    else:
        products = Product.objects.filter(available=True)
        category = None
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category
    }
    return render(request, 'products/list.html', context)

def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, available=True)
    
    # Get related products (same category, excluding current)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'products/details.html', {
        'product': product
    })

@login_required
def add_to_cart(request):
    """Add product to cart"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            
            print(f"Adding product {product_id} quantity {quantity} for user {request.user.username}")  # Debug
            
            product = get_object_or_404(Product, id=product_id)
            
            # Get or create active cart
            cart, created = Cart.objects.get_or_create(
                user=request.user, 
                is_active=True
            )
            print(f"Cart: {cart.id}, Created: {created}")  # Debug
            
            # Add or update cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                product=product
            )
            
            if not created:
                cart_item.quantity += quantity
                print(f"Updated existing item, new quantity: {cart_item.quantity}")  # Debug
            else:
                cart_item.quantity = quantity
                print(f"Created new item with quantity: {quantity}")  # Debug
                
            cart_item.save()
            
            # Verify item was saved
            saved_item = CartItem.objects.filter(id=cart_item.id).first()
            print(f"Verified item in DB: {saved_item is not None}")  # Debug
            
            return JsonResponse({
                'success': True,
                'cart_count': cart.items.count(),
                'message': f'{product.name} added to cart!',
                'item_id': cart_item.id
            })
            
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
@login_required
def cart_view(request):
    """View cart page"""
    try:
        # Get active cart for user
        cart = Cart.objects.get(user=request.user, is_active=True)
        items = cart.items.all()
        total = sum(item.product.price * item.quantity for item in items)
        
        print(f"Cart found: {cart.id}, Items: {items.count()}")  # Debug print
        
    except Cart.DoesNotExist:
        # Create new cart if none exists
        cart = Cart.objects.create(user=request.user, is_active=True)
        items = []
        total = 0
        print("New cart created")  # Debug print
    
    context = {
        'cart': cart,
        'items': items,
        'total': total
    }
    return render(request, 'products/cart.html', context)

@login_required
def update_cart(request):
    """Update cart item quantity"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = data.get('quantity')
            
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            
            # Recalculate cart total
            cart = cart_item.cart if quantity > 0 else Cart.objects.get(user=request.user, is_active=True)
            total = sum(item.product.price * item.quantity for item in cart.items.all())
            
            return JsonResponse({
                'success': True,
                'total': float(total),
                'cart_count': cart.items.count()
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
from django.http import HttpResponse

def debug_cart(request):
    """Debug view to check cart contents"""
    if not request.user.is_authenticated:
        return HttpResponse("Please login first")
    
    carts = Cart.objects.filter(user=request.user)
    output = f"<h1>Cart Debug for {request.user.username}</h1>"
    
    for cart in carts:
        output += f"<h3>Cart ID: {cart.id}, Active: {cart.is_active}</h3>"
        items = cart.items.all()
        if items:
            output += "<ul>"
            for item in items:
                output += f"<li>{item.product.name} - Quantity: {item.quantity} - Price: ₹{item.product.price}</li>"
            output += "</ul>"
        else:
            output += "<p>No items in this cart</p>"
    
    return HttpResponse(output)