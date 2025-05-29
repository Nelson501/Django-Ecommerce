from django.contrib import admin
from .models import ShippingAddress, Order, Order_items


# register the model

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(Order_items)
