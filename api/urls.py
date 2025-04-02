from django.urls import path
from .views import *


urlpatterns = [
    path('restaurants/', RestaurantView.as_view(), name='restaurant-create'),
]