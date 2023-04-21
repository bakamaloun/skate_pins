from django.shortcuts import render
from .models import Pin, PinReview
from .serializers import PinSerializer, PinReviewSerializer, PinListSerializer
from .permissions import IsEditorPermission
from api.authentication import TokenAuth
from rest_framework import generics, permissions, authentication
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

#create and list APIs
class PinListCreateAPIView(generics.ListCreateAPIView):

    #for list - only id and coordinates
    queryset = Pin.objects.filter(is_approved=True)
    serializer_class = PinListSerializer
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]
    permission_classes = [IsEditorPermission]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PinSerializer
        return PinListSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

#detail view API
class PinDetailAPIView(generics.RetrieveAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]

#update API
class PinUpdateAPIView(generics.UpdateAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]
    permission_classes = [IsEditorPermission]
    lookup_field = 'pk'

    def make_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

#delete API
class PinDeleteAPIView(generics.DestroyAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]
    permission_classes = [IsEditorPermission]
    lookup_field = 'pk'

    def make_delete(self, instance):
        super().perform_destroy(instance)

#create API
class PinCreateAPIView(generics.CreateAPIView):
    parser_class = [MultiPartParser, FormParser]
    serializer_class = PinSerializer

#view list API
class PinListAPIView(generics.ListAPIView):

    queryset = Pin.objects.filter(is_approved = True)
    serializer_class = PinSerializer
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]
    def get_queryset(self):
        qs = super().get_queryset()
        return qs

#create Pin Review
class PinReviewCreateAPIView(generics.CreateAPIView):
    queryset = PinReview.objects.all()
    serializer_class = PinReviewSerializer
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]
    permission_classes = [IsEditorPermission]

#Reviews of pins with filter
class ReviewsOfPinAPIView(generics.ListAPIView):
    queryset = PinReview.objects.all()
    serializer_class = PinReviewSerializer
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pin']

#average rating for pin

class MyPinsAPIView(generics.ListAPIView):
    serializer_class = PinSerializer
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]

    def get_queryset(self):
        user = self.request.user.id
        return Pin.objects.filter(created_by=user, is_approved=True)