from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe

# Create your models here.

def upload_to(instance, filename):
    return 'pins/{filename}'.format(filename=filename)

class Pin(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now(), editable=False)
    content = models.TextField(blank=True, null=True)
    #1-3 images, 1 req, remove def
    #image = models.ImageField(upload_to=upload_to, default='pins/default.jpg')
    latitude = models.CharField(max_length=100, default='0.0')
    longitude = models.CharField(max_length=100, default='0.0')
    created_by = models.ForeignKey(User, related_name='Pins', on_delete=models.CASCADE, null=True)
    #approved, def=F
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class PinImages(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return '%r images' % (self.pin.id)

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


    #reviews - new model
    #text - not req
    #rating (1-5) req
    #bust(1-5) req

class PinReview(models.Model):
    RATING_CHOICES = [
                        (1, 1),
                        (2, 2),
                        (3, 3),
                        (4, 4),
                        (5, 5)
                        ]
    review = models.TextField(blank=True, null=True)
    pin = models.ForeignKey(Pin, related_name='Pins', on_delete=models.CASCADE, null=True, blank=True)
    #change to float
    rating = models.FloatField(max_length=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    bust = models.FloatField(max_length=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    created_by = models.ForeignKey(User, related_name='Reviews', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'%r  {self.review}' % (self.pin)