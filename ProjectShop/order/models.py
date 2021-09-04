from django.db import models
from django.contrib.auth import get_user_model


from UserApp.models import User


# Create your models here.
class Order(models.Model):
    """Create Order model and take information about order.

    order_date: Date of order creation (auto);
    type: datetime, autofield.

    payment_method: customer payment method.
    (1:Card, 2:Cash), type: int, default: 2.

    user: User's ID for the order.
    type: int, foreign key from User.

    shipping_status: Status of the order.
    (1, "Planning"), (2, "Shipping"), (3, "Complete").
    type: int, default: 1

    payment_status: Payment status of the order.
    (1, "Pending"), (2, "Paid").
    type: int, default: 1

    """
    order_date = models.DateTimeField(auto_now_add=True)
    PAYMENT_METHODS = (
        (1, "Card"),
        (2, "Cash")
    )
    payment_method = models.IntegerField(verbose_name="Payment Method", choices=PAYMENT_METHODS, default=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # shippingAddress_id = models.ForeignKey("ShippingAddress", on_delete=models.CASCADE)
    SHIPPING_STATUSES = (
        (1, "Planning"),
        (2, "Shipping"),
        (3, "Complete")
    )
    shipping_status = models.IntegerField(verbose_name="Shipping status", choices=SHIPPING_STATUSES, default=1)
    PAYMENT_STATUSES = (
        (1, "Pending"),
        (2, "Paid")
    )
    payment_status = models.IntegerField(verbose_name="Payment Status", choices=PAYMENT_STATUSES, default=1)


