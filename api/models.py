from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count, Sum, Min, Max

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=255)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    opening_hours = models.CharField(max_length=255)
    price_range = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reservations', on_delete=models.CASCADE)
    customer_name = models.CharField(User,max_length=255)
    reservation_date = models.DateTimeField()
    number_of_people = models.IntegerField()

    def __str__(self):
        return f"{self.customer_name} - {self.restaurant.name}"
    
class Chef(models.Model):
    name=models.CharField(max_length=255,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    experience=models.IntegerField(null=True,blank=True)
    
class Food(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_vegetarian = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    restaurant=models.ForeignKey(Restaurant, related_name='orders', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    food_items = models.ManyToManyField(Food, related_name='orders')
    
class Payment(models.Model):
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Cash', 'Cash')])
    payment_status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Failed', 'Failed')])
    transaction_id = models.CharField(max_length=255, unique=True) 