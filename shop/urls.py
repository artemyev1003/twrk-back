from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView


urlpatterns = [
    path('products/', ProductListAPIView.as_view()),
    path('products/<str:sku>/', ProductDetailAPIView.as_view()),
]
