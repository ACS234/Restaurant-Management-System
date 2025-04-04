from django.urls import path
from .views import (
    RestaurantAPIView, RestaurantQRAPIView, FoodAPIView, OrderAPIView, 
    OrderItemAPIView, OrderStatusAPIView, PaymentAPIView, GenerateReceiptAPIView,
    ReviewAPIView,  InventoryAPIView
)

urlpatterns = [
<<<<<<< HEAD
    path('restaurants/', RestaurantView.as_view(), name='restaurant-create'),
    path('food/',FoodView.as_view(),name='food-list'),
    path('food/<int:pk>/',FoodUpdateView.as_view(),name='food-update'),
    path('order/',OrderView.as_view(),name="order-details")
=======
    path('restaurants/', RestaurantAPIView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/qr/', RestaurantQRAPIView.as_view(), name='restaurant_qr'),
    path('foods/', FoodAPIView.as_view(), name='food_list'),
    path('orders/', OrderAPIView.as_view(), name='order_list'),
    path('orders/items/', OrderItemAPIView.as_view(), name='order_item'),
    path('orders/<int:order_id>/status/', OrderStatusAPIView.as_view(), name='order_status'),
    path('payments/', PaymentAPIView.as_view(), name='payment'),
    path('orders/<int:order_id>/receipt/', GenerateReceiptAPIView.as_view(), name='generate_receipt'),
    path('reviews/', ReviewAPIView.as_view(), name='review_list'),
    path('inventory/', InventoryAPIView.as_view(), name='inventory'),
>>>>>>> e7454aaf5bb61465a95885c4bc1a435285916106
]
