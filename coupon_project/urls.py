from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('coupon_app/', include('coupon_app.urls')),  # Ensure this line is correct
]