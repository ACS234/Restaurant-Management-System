from django.db import models
from django.core.validators import MinValueValidator
import qrcode
from io import BytesIO
from django.utils import timezone
from django.core.files.base import ContentFile

class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.TextField()
    contact_number = models.CharField(max_length=15)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)

    # def generate_qr_code(self):
    #     qr = qrcode.make(f"Restaurant Menu: {self.name}")
    #     buffer = BytesIO()
    #     qr.save(buffer, format="PNG")
    #     self.qr_code.save(f"qr_{self.id}.png", ContentFile(buffer.getvalue()), save=False)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.generate_qr_code()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name


 
class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reservations', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255,null=True,blank=True)
    reservation_date = models.DateTimeField(null=True, blank=True)
    number_of_people = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.restaurant.name}"
    
class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='restaurants', on_delete=models.CASCADE,default=None)
    name=models.CharField(max_length=255,null=True,blank=True)
    price=models.IntegerField(validators=[MinValueValidator(10)])
  
    
    def __str__(self):
        return self.name

class Menu(models.Model):
    title = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField()
    available_from = models.DateTimeField(null=True, blank=True)
    available_to = models.DateTimeField(null=True, blank=True)
    foods = models.ManyToManyField(Food, related_name='menus',default=None)  # Many-to-Many Relationship

    def __str__(self):
        return self.title

class Order(models.Model):
    restaurant=models.ForeignKey(Restaurant, related_name='orders', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255,null=True,blank=True)
    order_date = models.DateTimeField(default=timezone.now)
    order_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],default='Pending')
    food_items = models.ManyToManyField(Menu, related_name='orders')
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
    
    
    
class OrderItem(models.Model):
    pass
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('UPI', 'UPI'),
        ('Wallet', 'Wallet')
    ])
    is_paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {'Paid' if self.is_paid else 'Pending'}"

class Receipt(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="receipt")
    pdf_file = models.FileField(upload_to="receipts/", blank=True, null=True)

    def __str__(self):
        return f"Receipt for Order {self.order.id}"

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(validators=[MinValueValidator(1)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.restaurant.name} - {self.rating}/5"
