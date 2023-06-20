from django.contrib import admin
from .models import Pin, PinReview, PinImages, PinEdit, Favourite

# Register your models here.

#admin.site.register(Pin)
admin.site.register(PinReview)
admin.site.register(PinImages)
admin.site.register(PinEdit)
admin.site.register(Favourite)

class PinImageInline(admin.TabularInline):
    model = PinImages
    readonly_fields = ('id', 'image_tag',)
    extra = 1

class PinEditInline(admin.TabularInline):
    model = PinEdit
    extra = 0

@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    inlines = [PinImageInline, PinEditInline]