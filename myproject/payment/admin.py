from django.contrib import admin
from .models import ShippingAddress, Order, Order_items
from django.contrib.auth.models import User


# register the model

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(Order_items)


class OrderItemInLine(admin.StackedInline):
    model = Order_items
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped"]
    inlines =[OrderItemInLine]


admin.site.unregister(Order)



admin.site.register(Order, OrderAdmin)
