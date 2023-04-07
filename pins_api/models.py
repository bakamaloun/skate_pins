from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone

# Create your models here.

def upload_to(instance, filename):
    return 'pins/{filename}'.format(filename=filename)

class Pin(models.Model):

    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now(), editable=False)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_to, default='pins/default.jpg')
    latitude = models.CharField(max_length=100, default='0.0')
    longitude = models.CharField(max_length=100, default='0.0')