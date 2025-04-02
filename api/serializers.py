from rest_framework import serializers
<<<<<<< HEAD
from .models import Restaurant,Menu,Reservation,Chef,Food,Order,Payment

# create modelserializer for Resturant
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Restaurant
        fields='__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Menu
        fields="__all__"

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields="__all__"

class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model=Chef
        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields="__all__"
=======
from .models import *
from django.contrib.auth.models import User 
from rest_framework.authtoken.models import Token
from django.utils import timezone

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
>>>>>>> 2cea6bea60efb255d48c51f1b9ed8ad8eb77c3bd
