from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Restaurant, Food, OrderItem, Order, Receipt, Payment, Review
)
from .serializers import (
    RestaurantSerializer, FoodSerializer, OrderItemSerializer,
    OrderSerializer, ReceiptSerializer, PaymentSerializer, ReviewSerializer
)
from django.template.loader import render_to_string
import pdfkit
import os
from django.conf import settings

# Restaurant API
class RestaurantAPIView(APIView):
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

class RestaurantQRAPIView(APIView):
    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        return FileResponse(open(restaurant.qr_code.path, "rb"), content_type="image/png")

# Food API
class FoodAPIView(APIView):
    def get(self, request):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Order API
class OrderAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Order Item API
class OrderItemAPIView(APIView):
    
    def get(self, request):
        # order_items = OrderItem.objects.filter(order=request.GET.get("order_id"))
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Order Status API
class OrderStatusAPIView(APIView):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        return Response({"order_status": order.status})

    def patch(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.status = request.data.get("status", order.status)
        order.save()
        return Response({"message": "Order status updated", "status": order.status})

# Payment API
class PaymentAPIView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data.get('order')

            # Ensure order is not already paid
            if Payment.objects.filter(order=order).exists():
                return Response({"error": "Payment already exists"}, status=status.HTTP_400_BAD_REQUEST)

            payment = serializer.save()
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Receipt API (PDF Generation)
class GenerateReceiptAPIView(APIView):
    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        # Check if receipt already exists
        if Receipt.objects.filter(order=order).exists():
            receipt = Receipt.objects.get(order=order)
            return FileResponse(open(receipt.pdf_file.path, "rb"), content_type="application/pdf")

        # Generate PDF
        context = {"order": order, "items": order.items.all()}
        html_content = render_to_string("receipt_template.html", context)

        pdf_file_path = os.path.join(settings.MEDIA_ROOT, f"receipts/order_{order_id}.pdf")
        pdfkit.from_string(html_content, pdf_file_path)

        # Save receipt in database
        receipt = Receipt.objects.create(order=order, pdf_file=f"receipts/order_{order_id}.pdf")

        return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")

# Review API
class ReviewAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Inventory API (Track Ingredients)
class InventoryAPIView(APIView):
    def get(self, request):
        foods = Food.objects.all()
        inventory = {food.name: food.stock_quantity for food in foods}
        return Response(inventory)

    def patch(self, request):
        food = get_object_or_404(Food, id=request.data.get("food_id"))
        food.stock_quantity = request.data.get("stock_quantity", food.stock_quantity)
        food.save()
        return Response({"message": "Inventory updated", "food": food.name, "stock": food.stock_quantity})
