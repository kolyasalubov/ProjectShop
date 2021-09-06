from django.db import models

from django_countries.fields import CountryField

class ShippingModel(models.Model):
    # shipping_address_id = models.IntegerField(verbose_name="shipping address Id", primary_key=True)
    postal_code = models.CharField(verbose_name="postal code", null=False, blank=False, max_length=20)
    country = CountryField()
    region = models.CharField(verbose_name="region", null=False, blank=False, max_length=50)
    city = models.CharField(verbose_name="city", null=False, blank=False, max_length=50)
    post_office = models.IntegerField(verbose_name="post office", null=False, blank=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Shipping address'
        verbose_name_plural = 'Shipping addresses'

    def __str__(self):
        return str({
            "postal_code": self.postal_code,
            "country": self.country,
            "region": self.region,
            "city": self.city,
            "post_office": self.post_office
        })