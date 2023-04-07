from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('auth/', ObtainAuthToken.as_view()),
    path('register/', views.RegisterView.as_view(), name='auth_register'),

]