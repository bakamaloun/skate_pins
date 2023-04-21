from django.contrib import admin
from .models import Pin, PinReview, PinImages

# Register your models here.

#admin.site.register(Pin)
admin.site.register(PinReview)
admin.site.register(PinImages)

class PinImageInline(admin.TabularInline):
    model = PinImages
    readonly_fields = ('id', 'image_tag',)
    extra = 1

@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    inlines = [PinImageInline]