from django.contrib import admin

from order.models import Order
from order.models import OrderItems


admin.site.register(Order)
admin.site.register(OrderItems)


