from django.db import models
from django.core.validators import *


class ProductCategory(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)


class ProductSubcategory(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)


class Tag(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)


class Product(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(validators=[MinValueValidator(0)], decimal_places=2, null=False, blank=False)
    description = models.TextField(max_length=5000, null=False, blank=False)
    stock_quantity = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)
    category = models.ManyToManyField(ProductCategory)
    subcategory = models.ManyToManyField(ProductSubcategory)
    tags = models.ManyToManyField(Tag)


class Review(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator[0], MaxValueValidator(5)], null=False, blank=False)
    comment = models.TextField(max_length=5000, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    # user = add user object reference here...


class ProductMedia(models.Model):

    MEDIA_TYPES = [
        (0, 'picture'),
        (1, 'video_link')
    ]

    media_type = models.IntegerField(choices=MEDIA_TYPES, null=False, blank=False)
    image = models.ImageField(upload_to="", null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)
    product = models.ForeignKey(Product, blank=False, null=False, on_delete=models.PROTECT)



