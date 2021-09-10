from django.db import models

from UserApp.models import User


class WishList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # products = models.ManyToManyField(Product, related_name='wishlists')