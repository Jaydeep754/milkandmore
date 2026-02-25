from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_views.home, name='home'),  # Homepage
    path('accounts/', include('accounts.urls')),  # Authentication URLs
    path('products/', include('products.urls')),  # Product URLs
    path('orders/', include('orders.urls')),  # Order URLs
    path('delivery/', include('delivery.urls')),  # Delivery URLs
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)