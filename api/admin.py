from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(Menu)
admin.site.register(Food)
admin.site.register(Payment)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Receipt)

