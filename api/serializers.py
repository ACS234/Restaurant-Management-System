from rest_framework import serializers
<<<<<<< HEAD
from .models import Restaurant,Menu,Reservation,Chef,Food,Order,Payment
=======
from .models import *
>>>>>>> e794a4ce405600712ebd18d54a02b09cd3b4feec

# create modelserializer for Resturant
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Restaurant
        fields='__all__'


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
