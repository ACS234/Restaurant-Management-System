from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count, Sum, Min, Max



# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255,null=True, blank=True)
    location = models.CharField(max_length=255,null=True, blank=True)
    cuisine_type = models.CharField(max_length=255,null=True, blank=True)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    opening_hours = models.CharField(max_length=255, null=True, blank=True)
    price_range = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
<<<<<<< HEAD

 
=======
>>>>>>> e794a4ce405600712ebd18d54a02b09cd3b4feec
class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reservations', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255,null=True,blank=True)
    reservation_date = models.DateTimeField(null=True, blank=True)
    number_of_people = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.restaurant.name}"
    
class Chef(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='restaurants', on_delete=models.CASCADE)
    name=models.CharField(max_length=255,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    experience=models.IntegerField(null=True,blank=True)
    order=models.ForeignKey('Order',related_name='chef',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Food(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    restaurant = models.ForeignKey(Restaurant, related_name='food_items', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    food_image = models.ImageField(upload_to='food_images/', null=True, blank=True)
    is_vegetarian = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    restaurant=models.ForeignKey(Restaurant, related_name='orders', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255,null=True,blank=True)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    food_items = models.ManyToManyField(Food, related_name='orders')
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
    
    
    def calculate_total_amount(self):
        total = sum(food_item.price for food_item in self.food_items.all())
        self.total_amount = total
        self.save()
        return total
    
class Payment(models.Model):
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Cash', 'Cash')])
    payment_status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Failed', 'Failed')])
    transaction_id = models.CharField(max_length=255, unique=True) 
    
    
    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.payment_status}"