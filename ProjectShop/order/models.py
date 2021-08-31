from django.db import models

# Create your models here.
class Order(models.Model):
    order = models.IntegerField(verbose_name="ID", primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    PAYMENT_METHODS = (
        (1, "Card"),
        (2, "Cash")
    )
    payment_method = models.IntegerField(verbose_name="Payment Method", choices=PAYMENT_METHODS)