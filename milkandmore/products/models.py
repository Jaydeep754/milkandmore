from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ['slug', 'parent']  # Prevents duplicate slugs under same parent
    
    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
    
    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])
    
    @property
    def is_subcategory(self):
        return self.parent is not None
    
    @property
    def get_all_products(self):
        """Get all products in this category and subcategories"""
        categories = [self]
        if self.children.exists():
            categories.extend(self.children.all())
        return Product.objects.filter(category__in=categories, available=True)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # Dairy specific fields
    is_milk = models.BooleanField(default=False)
    fat_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    volume_ml = models.IntegerField(null=True, blank=True)
    expiry_days = models.IntegerField(default=3)
    flavor = models.CharField(max_length=50, blank=True, null=True)  # For flavored products like lassi
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])