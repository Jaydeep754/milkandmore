from django.db import models
from django.conf import settings
from orders.models import Order

# If you have delivery-specific models, add them here
# For now, we can leave this empty or add a simple model

class DeliveryRoute(models.Model):
    delivery_boy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_delivery_boy': True})
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sequence = models.IntegerField(default=1)
    estimated_time = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Route for {self.delivery_boy.username} - Order #{self.order.id}"