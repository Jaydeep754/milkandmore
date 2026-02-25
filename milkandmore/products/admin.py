from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created')
    list_filter = ('available', 'category', 'is_milk')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'description', 'image')
        }),
        ('Pricing and Stock', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Dairy Specific', {
            'fields': ('is_milk', 'fat_percentage', 'volume_ml', 'expiry_days'),
            'classes': ('collapse',)
        }),
    )