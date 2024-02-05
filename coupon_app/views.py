from django.shortcuts import render
from django.http import HttpResponse
from .models import Coupon, Device
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import uuid
import base64
# ... import other necessary modules ...

def home(request):
    return render(request, 'home.html')

def generate_qr_code(request):
    data = request.build_absolute_uri('/coupon_app/coupon/')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_url = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'qr_code_page.html', {'qr_code_url': qr_code_url})


import hashlib
from django.shortcuts import render
from django.http import HttpResponse
from .models import Coupon, Device

# ... include your other necessary imports ...
import logging

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_device_fingerprint(request):
    ip_address = get_client_ip(request)
    screen_resolution = request.COOKIES.get('screen_resolution', '')

    fingerprint = f"{ip_address}-{screen_resolution}"
    return fingerprint

def hash_fingerprint(fingerprint):
    return hashlib.sha256(fingerprint.encode()).hexdigest()


from django.core.cache import cache

def coupon_page(request):
    fingerprint = get_device_fingerprint(request)
    hashed_fingerprint = hash_fingerprint(fingerprint)
    # Log the fingerprint
    logging.info(f"Generated fingerprint: {hashed_fingerprint}")

    # Rate limiting based on IP address
    ip_address = get_client_ip(request)
    cache_key = f"coupon_claim_{ip_address}"
    if cache.get(cache_key):
        return render(request, 'coupon_page.html', {'coupon_claimed': True})

    device, created = Device.objects.get_or_create(device_id=hashed_fingerprint)
    if not created and device.coupon:
        # Existing device with a coupon
        return render(request, 'coupon_page.html', {'coupon_number': device.coupon.number})
    else:
        # New device or device without a coupon
        unused_coupon = Coupon.objects.filter(is_used=False).first()
        if unused_coupon:
            unused_coupon.is_used = True
            unused_coupon.save()
            device.coupon = unused_coupon
            device.save()
            return render(request, 'coupon_page.html', {'coupon_number': unused_coupon.number})
        else:
            return render(request, 'coupon_page.html', {'all_coupons_distributed': True})
        
    cache.set(cache_key, True, 86400)
# ... include your other views ...
