from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem, DeliveryStatus

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price')

class DeliveryStatusInline(admin.TabularInline):
    model = DeliveryStatus
    readonly_fields = ('status', 'timestamp', 'updated_by', 'notes')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'order_date', 'delivery_boy')
    list_filter = ('status', 'payment_method', 'order_date')
    search_fields = ('user__username', 'user__email', 'delivery_address')
    readonly_fields = ('order_date',)
    inlines = [OrderItemInline, DeliveryStatusInline]
    actions = ['mark_as_confirmed', 'mark_as_delivered']

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected orders as confirmed"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = "Mark selected orders as delivered"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('product__name',)