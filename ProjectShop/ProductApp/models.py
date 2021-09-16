from django.db import models
from django.core.validators import *
from UserApp.models import User


class ProductCategory(models.Model):

    """
    A database objects that represents a category of items.
    (Like large groups: TVs, phones, tables, etc... SUBJECT TO CHANGE.)

    Attributes:
        name: name of the category.
    """

    name = models.CharField(max_length=100, null=False, blank=False)


class ProductSubcategory(models.Model):
    """
    A database object that represents a smaller subcategory of items.
    (Like small subgroups: brands, subtypes, etc... SUBJECT TO CHANGE.)

    Attributes:
        name: name of the subcategory.
    """

    name = models.CharField(max_length=100, null=False, blank=False)


class Tag(models.Model):
    """
    A database object that represents a string-like tag bound to items.
    (Diverse, anything that can be useful, and is matched by similarity and not equality ... SUBJECT TO CHANGE.)

    Attributes:
        name: the name of the tag.
    """

    name = models.CharField(max_length=100, null=False, blank=False)


class Product(models.Model):
    """
    A database object that represents a product that the shop might have for sale,
    based on current availability.

    Attributes:
        name: short, informative description, name of the product.
        price: product price.
        description: a detailed description of the product.
        stock_quantity: amount of subject products currently in stock.
        categories: references to categories that subject product belongs to.
        subcategories: references to subcategories that subject product belongs to.
        tags: references to tags that subject is assigned.
    """

    subcategories = models.ManyToManyField(ProductSubcategory)
    categories = models.ManyToManyField(ProductCategory)
    tags = models.ManyToManyField(Tag)

    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(validators=[MinValueValidator(0)], decimal_places=2, null=False, blank=False)
    description = models.TextField(max_length=5000, null=False, blank=False)
    stock_quantity = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)


class Review(models.Model):
    """
    A database object that represents a review left by a user,
    including a numeric rating (0 - 5 stars), and a comment (optional).

    Attributes:
        rating: numeric rating left by user, or as they are commonly known - "stars" (0 - 5).
        comment: a text review of product left by user (optional).
        product: reference to the reviewed product.
        user: reference to the user writing a review.
    """

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    rating = models.IntegerField(validators=[MinValueValidator[0], MaxValueValidator(5)], null=False, blank=False)
    comment = models.TextField(max_length=5000, null=True, blank=True)



class ProductMedia(models.Model):
    """
    A database object that represents media bound to the product, like pictures or video links.

    Attributes:
        media_type: indicates whether media is a picture or a video iframe.
        image: reference to image saved in django 'media' file.
        video_link: link to data that iframe is using.
        product: reference to target product.
    """

    MEDIA_TYPES = [
        (0, 'picture'),
        (1, 'video_link')
    ]

    product = models.ForeignKey(Product, blank=False, null=False, on_delete=models.PROTECT)

    media_type = models.IntegerField(choices=MEDIA_TYPES, null=False, blank=False)
    image = models.ImageField(upload_to="", null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)



