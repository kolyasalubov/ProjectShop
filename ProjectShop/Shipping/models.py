from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from UserApp.models import User


class ShippingModel(models.Model):
    """
    Class for shipping address model

    Attributes:

    postal_code: Describes postal code
    type: str, max_length=20
    country: Describes to which country make a delivery
    type: CountryField (https://pypi.org/project/django-countries/)
    region: Describes to which region make a delivery
    type: str, max_length=50
    city: Describes to which city make a delivery
    type: str, max_length=50
    post_office: Describes which post office department
    type: int
    """

    # shipping_address_id = models.IntegerField(
    #     verbose_name="shipping address Id", primary_key=True
    # )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postal_code = models.CharField(
        verbose_name=_("postal code"), max_length=10
    )
    country = CountryField()
    region = models.CharField(
        verbose_name=_("region"), max_length=50
    )
    city = models.CharField(
        verbose_name=_("city"), max_length=50
    )
    post_office = models.IntegerField(
        verbose_name=_("post office")
    )

    class Meta:
        verbose_name = _("Shipping address")
        verbose_name_plural = _("Shipping addresses")

    def __str__(self):
        return str(
            {
                "postal_code": self.postal_code,
                "country": self.country,
                "region": self.region,
                "city": self.city,
                "post_office": self.post_office,
            }
        )
