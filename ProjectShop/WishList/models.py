from django.db import models

from UserApp.models import User
from ProductApp.models import Product


class WishList(models.Model):
    """
       A database object that represents products that user want to buy in future.
       Attributes:
           products: references to category that product belongs to.
           user: reference to the user who make wishlist.
       """

    products = models.ManyToManyField(Product, related_name='wishlists')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
