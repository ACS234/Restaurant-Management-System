from django.urls import path
from .views import *


urlpatterns = [
    path('restaurants/', RestaurantView.as_view(), name='restaurant-create'),
    path('food/',FoodView.as_view(),name='food-list'),
    path('food/<int:pk>/',FoodUpdateView.as_view(),name='food-update'),
    path('order/',OrderView.as_view(),name="order-details")
]
