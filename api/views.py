from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from .serializers import *
from .models import *
# Create your views here.


class RestaurantView(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodView(APIView):
    def get(self,request):
        food=Food.objects.all()
        serializer=FoodSerializer(food,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class FoodUpdateView(APIView):
    def get(self,request,pk):
        try:
            food=Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response({'Error':'food not found'},status=status.HTTP_404_NOT_FOUND)
        #Deserialize incoming data
        serializer=FoodSerializer(food)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            food=Food.objects.get(pk=pk)
        except:
            return Response({'Error':'food not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=FoodSerializer(food,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self,request,pk):
    #     try:
    #         food=Food.objects.get(pk=pk)
    #     except:
    #         return Response({'Error':'food not found'},status=status.HTTP_404_NOT_FOUND)
    #     food.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrderView(APIView):
    def post(self,request):
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    


