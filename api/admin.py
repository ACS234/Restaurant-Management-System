from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Reservation)
admin.site.register(Chef)
admin.site.register(Order)
admin.site.register(Food)
admin.site.register(Payment)

