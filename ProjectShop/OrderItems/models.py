from django.db import models
from django.utils.translation import gettext as _

from order.models import Order


class OrderItems(models.Model):
    """
        A database objects that represents items in order.
        Attributes:
            order_id: reference to the order.
            product_id: reference to the product.
            quantity: amount of products in order.
        """

    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    # product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(verbose_name=_("quantity"))
