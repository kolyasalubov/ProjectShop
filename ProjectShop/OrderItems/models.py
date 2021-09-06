from django.db import models
from django.utils.translation import gettext as _

from order.models import Order


# Create your models here.
class OrderItems(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    # product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_("quantity"))
