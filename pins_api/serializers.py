from rest_framework import serializers
from .models import Pin

class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = [
            'title',
            'id',
            'content',
            'created_at',
            'image',
            'latitude',
            'longitude'
        ]