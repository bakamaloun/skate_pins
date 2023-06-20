from rest_framework import serializers
from .models import Pin, PinReview, PinImages, PinEdit, Favourite
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator

class PinImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PinImages
        fields = '__all__'

class PinSerializer(serializers.ModelSerializer):

    images = PinImageSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        max_length=3
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
            'uploaded_images',
            'is_approved',
            'avg_rating',
            'avg_bust'
        ]

        read_only_fields = ['created_by']

    avg_rating = serializers.SerializerMethodField()

    def get_avg_rating(self, ob):
        # reverse check for reviews score
        return ob.Pins.all().aggregate(Avg('rating'))['rating__avg']

    avg_bust = serializers.SerializerMethodField()

    def get_avg_bust(self, ob):
        # reverse check for bust score
        return ob.Pins.all().aggregate(Avg('bust'))['bust__avg']

    # def validate_uploaded_images(self, value):
    #     if len(value) > 3:
    #         raise serializers.ValidationError('too much images')
    #     return value

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        pin = Pin.objects.create(**validated_data)

        for image in uploaded_images:
            PinImages.objects.create(pin=pin, image=image)

        return pin

    def clear_existing_images(self, instance, validated_data):
        for pin_image in instance.images.order_by('-id').all()[3:]:
            pin_image.image.delete()
            pin_image.delete()

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')

        if uploaded_images:

            uploaded_images = (PinImages(pin=instance, image=image) for image in uploaded_images)
            PinImages.objects.bulk_create(uploaded_images)
            self.clear_existing_images(instance, validated_data)

        return super().update(instance, validated_data)


class PinListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pin
        fields = [
            'name',
            'id',
            'latitude',
            'longitude',
            'is_approved'
        ]

class PinReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinReview
        fields = [
            'review',
            'pin',
            'rating',
            'bust',
            'created_by'
        ]

        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

        validators = [
            UniqueTogetherValidator(
                queryset=PinReview.objects.all(),
                fields=['pin', 'created_by'],
                message='only 1 review per user'
            )
        ]

class PinEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinEdit
        fields = [
            'name',
            'id',
            'content',
            'created_at',
            'created_by',
            'pin'
        ]

        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = [
            'user',
            'pin',
            'id'
        ]

        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}

        validators = [
            UniqueTogetherValidator(
                queryset=Favourite.objects.all(),
                fields=['pin', 'user'],
                message='cant add to fav more than once'
            )
        ]