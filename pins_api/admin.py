from django.contrib import admin
from .models import Pin, PinReview, PinImages

# Register your models here.

admin.site.register(Pin)
admin.site.register(PinReview)
admin.site.register(PinImages)