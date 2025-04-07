from django.urls import path
from .views import (
    RestaurantAPIView, RestaurantQRAPIView, FoodAPIView, OrderAPIView, 
    OrderItemAPIView, OrderStatusAPIView, PaymentAPIView, GenerateReceiptAPIView,
    ReviewAPIView, InventoryAPIView,MenuAPIView,MenuDetailAPIView,OrderDetailAPIView
)

urlpatterns = [
    path('restaurants/', RestaurantAPIView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/qr/', RestaurantQRAPIView.as_view(), name='restaurant_qr'),
    path('foods/', FoodAPIView.as_view(), name='food_list'),
    path('orders/', OrderAPIView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail'),
    path('menus/', MenuAPIView.as_view(), name='menu_list'),
    path('menus/<int:pk>/', MenuDetailAPIView.as_view(), name='menu_detail'),
    path('orders/items/', OrderItemAPIView.as_view(), name='order_item'),
    path('orders/<int:order_id>/status/', OrderStatusAPIView.as_view(), name='order_status'),
    path('payments/', PaymentAPIView.as_view(), name='payment'),
    path('orders/<int:order_id>/receipt/', GenerateReceiptAPIView.as_view(), name='generate_receipt'),
    path('reviews/', ReviewAPIView.as_view(), name='review_list'),
    path('inventory/', InventoryAPIView.as_view(), name='inventory'),
]
