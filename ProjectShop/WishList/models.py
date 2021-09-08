from django.db import models

from UserApp.models import User


class WishList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
