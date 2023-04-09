
from .serializers import RegisterSerializer
from rest_framework import generics, status, permissions, authentication
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from api.authentication import TokenAuth
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class Logout(GenericAPIView):
    authentication_classes = [authentication.SessionAuthentication,
                              TokenAuth]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)
