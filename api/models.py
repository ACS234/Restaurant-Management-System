from django.db import models
from django.core.validators import MinValueValidator
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True,null=True, blank=True)
    location = models.TextField(default="Write Location.",null=True, blank=True)
    contact_number = models.CharField(max_length=15,null=True, blank=True)
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


class Food(models.Model):
    FOOD_CHOICES = [
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
    ]
    food_category = models.CharField(max_length=100, choices=FOOD_CHOICES, default='Veg',null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(default="Write some Descriptions.",null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2,null=True, blank=True)
    ingredients = models.TextField(default="Write some Ingredients.",null=True, blank=True)
    image = models.ImageField(upload_to='foods/',null=True, blank=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(default="Write some descriptions.",null=True, blank=True)
    is_available = models.BooleanField(default=True)
    foods = models.ManyToManyField(Food, related_name='menus',default=None)  # Many-to-Many Relationship

    def __str__(self):
        return self.title

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,default=None)
    customer_name = models.CharField(max_length=255,null=True, blank=True)
    customer_contact = models.CharField(max_length=15,null=True, blank=True)
    food_items = models.ManyToManyField(Food, through='OrderItem',default=None) 
    delivery_address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True) 
    

    def __str__(self):
        return f"{self.quantity} x {self.food.name} Total Price {self.total_amount} (Order {self.order.id})"

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
