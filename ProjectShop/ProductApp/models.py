from django.db import models
from django.utils.html import format_html
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatewords

from UserApp.models import User


class ProductCategory(models.Model):
    """
    A database objects that represents a category of items.
    (Like large groups: TVs, phones, tables, etc... SUBJECT TO CHANGE.)

    Attributes:
        name: name of the category.
    """

    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name_plural = _("Product categories")

    def __str__(self):
        return self.name


class ProductSubcategory(models.Model):
    """
    A database object that represents a smaller subcategory of items.
    (Like small subgroups: brands, subtypes, etc... SUBJECT TO CHANGE.)

    Attributes:
        name: name of the subcategory.
    """

    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name_plural = _("Product subcategories")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    A database object that represents a string-like tag bound to items.
    (Diverse, anything that can be useful, and is matched
    by similarity and not equality ... SUBJECT TO CHANGE.)

    Attributes:
        name: the name of the tag.
    """

    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


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
    price = models.DecimalField(
        validators=[validators.MinValueValidator(0)],
        decimal_places=2,
        max_digits=9,
        null=False,
        blank=False,
    )
    description = models.TextField(max_length=5000, null=False, blank=False)
    stock_quantity = models.IntegerField(
        validators=[validators.MinValueValidator(0)], null=False, blank=False
    )

    def __str__(self):
        return self.name

    @property
    def short_description(self):
        return truncatewords(self.description, 20)


class Review(models.Model):
    """
    A database object that represents a review left by a user,
    including a numeric rating (0 - 5 stars), and a comment (optional).

    Attributes:
        rating: numeric rating left by user, or as they are
        commonly known - "stars" (0 - 5).
        comment: a text review of product left by user (optional).
        product: reference to the reviewed product.
        user: reference to the user writing a review.
    """

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    rating = models.IntegerField(
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(5)],
        null=False,
        blank=False,
    )
    comment = models.TextField(max_length=5000, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f"{self.user} review of {self.product}"


class Reply(models.Model):
    """
    A database object that represents a reply to review left by a user,
    including a like/dislike reaction.

    Attributes:
        reaction: numeric symbol which represent user reaction,
        where 1-like, 2-dislike, and 0 represents that he change his mind.
        review: reference to the review.
        user: reference to the user writing a review.
    """

    REACTIONS = [
        (0, "none"),
        (1, "like"),
        (2, "dislike"),
    ]

    review = models.ForeignKey(Review, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    reaction = models.PositiveSmallIntegerField(
        choices=REACTIONS, null=False, blank=False
    )

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f"{self.user} reply on {self.review} with reaction: {self.reaction}"


class ProductImage(models.Model):
    """
    A database object that represents images to the product.

    Attributes:
        image: reference to image saved in django 'media' file.
        product: reference to target product.
    """

    product = models.ForeignKey(
        Product, blank=False, null=False, on_delete=models.PROTECT, related_name="image"
    )

    image = models.ImageField(
        upload_to="product_media_image", default="default_image/default_image.png"
    )

    class Meta:
        verbose_name_plural = _("Product media")

    def small_image_tag(self):
        return format_html(
            '<img href="{0}" src="{0}" width="50" height="50" />'.format(self.image.url)
        )

    small_image_tag.allow_tags = True
    small_image_tag.short_description = _("Image")

    def image_tag(self):
        return format_html(
            '<img href="{0}" src="{0}" width="150" height="150" />'.format(
                self.image.url
            )
        )

    image_tag.allow_tags = True
    image_tag.short_description = _("Image")

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f"Image {self.id} of {self.product}"


class ProductVideo(models.Model):
    """
    A database object that represents video link to the product.

    Attributes:
        video_link: link to data that iframe is using.
        product: reference to target product.
    """

    product = models.ForeignKey(
        Product,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name="video_link",
    )

    video_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f"Video {self.id} of {self.product}"
