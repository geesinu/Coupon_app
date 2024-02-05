# delete_coupons.py

from coupon_app.models import Coupon

# Deleting all coupon entries
Coupon.objects.all().delete()

print("All coupons have been deleted.")
