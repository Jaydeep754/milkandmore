from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, DeliveryBoy

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_customer', 'is_delivery_boy', 'is_staff')
    list_filter = ('is_customer', 'is_delivery_boy', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address')}),
        ('User Type', {'fields': ('is_customer', 'is_delivery_boy')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'loyalty_points')
    search_fields = ('user__username', 'user__email')

@admin.register(DeliveryBoy)
class DeliveryBoyAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle_number', 'is_available', 'total_deliveries')
    list_filter = ('is_available',)
    search_fields = ('user__username', 'vehicle_number')