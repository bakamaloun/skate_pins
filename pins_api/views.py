from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Pin
from .serializers import PinSerializer
from .permissions import IsEditorPermission
from api.authentication import TokenAuth
from rest_framework import generics, permissions, authentication
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

#create and list APIs
class PinListCreateAPIView(generics.ListCreateAPIView):

    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]
    permission_classes = [IsEditorPermission]

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')

        if content is None:
            content = title
        serializer.save(content=content)

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
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]
    permission_classes = [IsEditorPermission]

#view list API
class PinListAPIView(generics.ListAPIView):

    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]
