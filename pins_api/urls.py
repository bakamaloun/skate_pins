from django.urls import path
from . import views

#/api/pins/
urlpatterns = [
    path('<int:pk>/', views.PinDetailAPIView.as_view()),
    path('<int:pk>/update/', views.PinUpdateAPIView.as_view()),
    path('<int:pk>/delete/', views.PinDeleteAPIView.as_view()),
    path('', views.PinListCreateAPIView.as_view()),
    path('create/', views.PinCreateAPIView.as_view()),
    path('all/', views.PinListAPIView.as_view()),
    path('add_review/', views.PinReviewCreateAPIView.as_view()),
]