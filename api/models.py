from django.db import models
from django.core.validators import MinValueValidator
import qrcode
from io import BytesIO
from django.utils import timezone
from django.core.files.base import ContentFile

class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True,null=True, blank=True)
    location = models.TextField(default="Write Location.",null=True, blank=True)
    contact_number = models.CharField(max_length=15,null=True, blank=True)
    opening_hours = models.CharField(max_length=100, default="9 AM - 11 PM",null=True)
    image = models.ImageField(upload_to="restaurant_images/", null=True, blank=True)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)


    def __str__(self):
        return self.name


<<<<<<< HEAD
 
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
=======

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    name = models.CharField(max_length=255,null=True,blank=True)  # Example: Breakfast, Lunch, Dinner
    category = models.CharField(max_length=255, null=True, blank=True)  # Example: Vegetarian, Non-Vegetarian
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="menu_images/", null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Allows enabling/disabling menus
>>>>>>> 31fa678b54e99200d8b5c8c4c30079f7ab6be694

    def __str__(self):
        return f"{self.name} Menu - {self.restaurant.name}"

class Food(models.Model):
    menu = models.ManyToManyField(Menu, related_name="foods")
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    ingredients = models.TextField(null=True,blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)  # Example: Appetizer, Main Course, Dessert
    is_vegetarian = models.BooleanField(default=False)
    image = models.ImageField(upload_to="food_images/", null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)],null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, validators=[MinValueValidator(0)])
    
    def __str__(self):
        menu_names = ", ".join([menu.name for menu in self.menu.all()])
        return f"{self.name} ({menu_names})"


class Order(models.Model):
<<<<<<< HEAD
    restaurant=models.ForeignKey(Restaurant, related_name='orders', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255,null=True,blank=True)
    order_date = models.DateTimeField(default=timezone.now)
    order_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],default='Pending')
    food_items = models.ManyToManyField(Menu, related_name='orders')
    
=======
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,default=None)
    customer_name = models.CharField(max_length=255,null=True, blank=True)
    customer_contact = models.CharField(max_length=15,null=True, blank=True)
    food_items = models.ManyToManyField(Food, through='OrderItem',default=None,related_name="orders") 
    delivery_address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

>>>>>>> 31fa678b54e99200d8b5c8c4c30079f7ab6be694
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
    
    
    
class OrderItem(models.Model):
<<<<<<< HEAD
    pass
=======
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    food = models.ForeignKey('Food', on_delete=models.CASCADE,related_name="order_items")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.food.name} (Order {self.order.id})"

    @property
    def total_price(self):
        # Dynamic property to calculate total price for item
        return self.food.price * self.quantity
    
>>>>>>> 31fa678b54e99200d8b5c8c4c30079f7ab6be694
class Payment(models.Model):
    PAYMENT_METHOD=[
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('UPI', 'UPI'),
        ('Wallet', 'Wallet')
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD,default='Cash')
    currency = models.CharField(max_length=10,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for Order {self.order.id} - {'Paid' if self.is_paid else 'Pending'} {self.amount}"

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
