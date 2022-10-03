from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductListAPIView, ProductDetailAPIView


urlpatterns = [
    path('products/', ProductListAPIView.as_view()),
    path('products/<str:sku>/', ProductDetailAPIView.as_view()),
]
