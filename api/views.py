import qrcode
import stripe
from io import BytesIO
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.template.loader import render_to_string
import pdfkit
import os
from django.conf import settings

# Imp data
# path_to_wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
stripe.api_key = settings.STRIPE_SECRET_KEY

# Restaurant API
class RestaurantAPIView(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = RestaurantSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        # Get the data from the request
        name = request.data.get('name')
        location = request.data.get('location')
        contact_number = request.data.get('contact_number')
        
        # Check if restaurant with the same name already exists
        if Restaurant.objects.filter(name=name).exists():
            return Response({"error": "A restaurant with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the restaurant
        restaurant = Restaurant.objects.create(
            name=name,
            location=location,
            contact_number=contact_number
        )
        
        # Generate the QR code
        qr = qrcode.make(f"Restaurant Menu: {restaurant.name}")
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        
        # Save the QR code to the restaurant model
        restaurant.qr_code.save(f"qr_{restaurant.id}.png", ContentFile(buffer.getvalue()), save=False)
        restaurant.save()  # Save again with the QR code

        # Serialize the response data
        serializer = RestaurantSerializer(restaurant)

        # Return the response with the restaurant data and QR code URL
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    

# Menu API
class MenuAPIView(APIView):
    def get(self, request):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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


class OrderItemAPIView(APIView):
    def get(self, request):
        order_id = request.GET.get("order_id")
        if order_id:
            order_items = OrderItem.objects.filter(order_id=order_id)
        else:
            order_items = OrderItem.objects.all()

        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            food_id = request.data.get("food")
            try:
                food = Food.objects.get(id=food_id)
            except Food.DoesNotExist:
                return Response({"detail": "Food not found"}, status=status.HTTP_404_NOT_FOUND)

            quantity = request.data.get("quantity")
            if not quantity:
                return Response({"detail": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Save the order item directly; total_price is calculated dynamically in the model/serializer
            order_item = serializer.save()
            return Response(OrderItemSerializer(order_item).data, status=status.HTTP_201_CREATED)

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
# class PaymentAPIView(APIView):
#     def post(self, request):
#         data = request.data
#         data["is_paid"] = True  # Set is_paid to True for new payments
        
#         serializer = PaymentSerializer(data=data)
#         if serializer.is_valid():
#             order = serializer.validated_data.get('order')
#             # Ensure order is not already paid
#             if Payment.objects.filter(order=order).exists():
#                 return Response({"error": "Payment already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
#             payment = serializer.save()
#             return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentAPIView(APIView):
    
    def get(self,request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        payment_method = data.get("payment_method")
        order = data.get("order")

        if Payment.objects.filter(order=order).exists():
            return Response({"error": "Payment already exists"}, status=400)

        if payment_method == "Stripe":
            payment_intent_id = data.get("payment_intent_id")

            if not payment_intent_id:
                return Response({"error": "Missing payment_intent_id"}, status=400)
            try:
                intent = stripe.PaymentIntent.retrieve(payment_intent_id)

                if intent.status != "succeeded":
                    return Response({"error": "Payment not completed"}, status=400)

                data["amount"] = intent.amount / 100
                data["currency"] = intent.currency
                data["stripe_id"] = intent.id
                data["is_paid"] = True
                data["payment_method"] = intent.payment_method

            except stripe.error.StripeError as e:
                return Response({"error": str(e)}, status=500)

        elif payment_method in ["Cash", "UPI", "Bank Transfer"]:
            if not data.get("amount"):
                return Response({"error": "Amount is required for non-Stripe payments"}, status=400)

            data["is_paid"] = True
            data["stripe_id"] = None 
            data["currency"] = data.get("currency", "INR") 

        else:
            return Response({"error": "Unsupported payment method"}, status=400)
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response(PaymentSerializer(payment).data, status=201)

        return Response(serializer.errors, status=400)

# Receipt API (PDF Generation)
class GenerateReceiptAPIView(APIView):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        items = order.items.all()

        items_data = []
        total = 0

        for item in items:
            subtotal = item.quantity * item.food.price
            item_data = {
                "name": item.id,
                "quantity": item.quantity,
                "unit_price": item.food.price,
                "subtotal": subtotal,
            }
            items_data.append(item_data)
            total += subtotal

        context = {
            "order_id": order.id,
            "restaurant": order.restaurant.name,
            "customer_name": order.customer_name,
            "date": order.created_at.strftime('%Y-%m-%d %H:%M'),
            "items": items_data,
            "total": total,
        }

        return render(request, "api/receipt.html", context)
    
    # def get(self, request, order_id):
    #     order = get_object_or_404(Order, pk=order_id)
    #     items = order.items.all()

    #     items_data = []
    #     total = 0

    #     for item in items:
    #         item_data = {
    #             "name": item.id,
    #             "quantity": item.quantity,
    #             "unit_price": item.food.price,
    #             "subtotal": item.quantity * item.food.price,
    #         }
    #         items_data.append(item_data)
    #         total += item_data["subtotal"]

    #     receipt_data = {
    #         "order_id": order.id,
    #         "customer_name": order.restaurant.name,
    #         "date": order.created_at.strftime('%Y-%m-%d %H:%M'),
    #         "items": items_data,
    #         "total": total,
    #     }

    #     return Response(receipt_data)
    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        html_content = render_to_string("api/receipt.html")

        # Check if receipt already exists
        if Receipt.objects.filter(order=order).exists():
            receipt = Receipt.objects.get(order=order)
            return FileResponse(open(receipt.pdf_file.path, "rb"), content_type="application/pdf")

        # Generate PDF
        try:
            pdf_file_path = os.path.join(settings.MEDIA_ROOT, f"receipts/order_{order_id}.pdf")
            pdfkit.from_string(html_content, pdf_file_path)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        # Save receipt in database
        receipt = Receipt.objects.create(order=order, pdf_file=f"receipts/order_{order_id}.pdf")

        return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")

# Review API
class ReviewAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Review complete successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
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