from rest_framework import serializers
from .models import Pin, PinReview, PinImages

class PinImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PinImages
        fields = "__all__"

class PinSerializer(serializers.ModelSerializer):

    images = PinImageSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Pin
        fields = [
            'name',
            'id',
            'content',
            'created_at',
            'latitude',
            'longitude',
            'created_by',
            'images',
            'uploaded_images'
        ]
        #extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        pin = Pin.objects.create(**validated_data)

        for image in uploaded_images:
            PinImages.objects.create(pin=pin, image=image)

        return pin

class PinReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinReview
        fields = [
            'review',
            'pin',
            'rating',
            'bust'
        ]