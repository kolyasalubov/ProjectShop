from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

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


    class PaymentMethod(models.TextChoices):
        CASH = "Cash", _("Cash")
        CARD = "Card", _("Card")

    payment_method = models.CharField(
                     max_length=4,
                     choices=PaymentMethod.choices,
                     default=PaymentMethod.CASH)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # shippingAddress_id = models.ForeignKey("ShippingAddress", on_delete=models.CASCADE)


    class ShippingStatus(models.TextChoices):
        PLANNING = "Planning", _("Planning")
        SHIPPING = "Shipping", _("Shipping")
        COMPLETED = "Completed", _("Completed")

    shipping_status = models.CharField(max_length=9,
                     choices=ShippingStatus.choices,
                     default=ShippingStatus.PLANNING)

    class PaymentStatus(models.TextChoices):
        PENDING = "Pending", _("Pending")
        PAID = "Paid", _("Paid")


    payment_status = models.CharField(max_length=7,
                     choices=PaymentStatus.choices,
                     default=PaymentStatus.PENDING)



