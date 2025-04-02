from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User 
from rest_framework.authtoken.models import Token
from django.utils import timezone

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'