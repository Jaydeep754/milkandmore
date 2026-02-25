from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_delivery_boy = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    loyalty_points = models.IntegerField(default=0)
    preferred_delivery_time = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.user.username

class DeliveryBoy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    vehicle_number = models.CharField(max_length=20, blank=True)
    is_available = models.BooleanField(default=True)
    total_deliveries = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username