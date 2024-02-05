from django.db import models

class Coupon(models.Model):
    number = models.CharField(max_length=4, unique=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.number
    
class Device(models.Model):
    device_id = models.CharField(max_length=256, unique=True)  # Adjust length as needed
    coupon = models.OneToOneField(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.device_id
