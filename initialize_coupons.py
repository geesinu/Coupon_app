# initialize_coupons.py

from coupon_app.models import Coupon
from django.db import IntegrityError

# Creating 10 coupon entries
for i in range(1, 11):
    coupon_number = str(i).zfill(3)  # Formats the number as 0001, 0002, etc.
    try:
        Coupon.objects.create(number=coupon_number)
    except IntegrityError:
        print(f"Coupon with number {coupon_number} already exists.")

print("Initialization complete.")
