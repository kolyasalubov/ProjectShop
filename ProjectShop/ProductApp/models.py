from django.core import validators
from django.db import models
from django.template.defaultfilters import truncatewords
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField
from ckeditor.fields import RichTextField

from UserApp.models import User


class ProductCategory(models.Model):
    """
    A database objects that represents a category of items.
    (Like large groups: TVs, phones, tables, etc... SUBJECT TO CHANGE.)

    Attributes:
        name: name of the category.
    """

    name = models.CharField(max_length=100, null=False, blank=False)
    slug = AutoSlugField(populate_from='name', editable=True)

    class Meta:
        verbose_name_plural = _("Product categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"slug": self.slug})


class ProductSubcategory(models.Model):
    """
    A database object that represents a smaller subcategory of items.
    (Like small subgroups: brands, subtypes, etc... SUBJECT TO CHANGE.)

    Attributes:
        name: name of the subcategory.
    """

    name = models.CharField(max_length=100, null=False, blank=False)
    slug = AutoSlugField(populate_from='name', editable=True)

    class Meta:
        verbose_name_plural = _("Product subcategories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("subcategory-detail", kwargs={"slug": self.slug})


class TagGroup(models.Model):
    """
    A database object that represents a group for grouping Tag instances.

    Attributes:
        name: group name.
    """

    name = models.CharField(max_length=100)

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
    slug = AutoSlugField(populate_from='name', editable=True)
    group = models.ForeignKey(TagGroup, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag-detail", kwargs={"slug": self.slug})


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
    slug = AutoSlugField(populate_from='name', editable=True)
    price = models.DecimalField(
        validators=[validators.MinValueValidator(0)],
        decimal_places=2,
        max_digits=9,
    )
    description = models.TextField(max_length=5000)
    stock_quantity = models.IntegerField(validators=[validators.MinValueValidator(0)])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"slug": self.slug})

    @classmethod
    def get_product_by_id(cls, product_id=1):
        return cls.objects.get(id=product_id)

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
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(5)]
    )
    
    comment = models.TextField(max_length=5000, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_review_by_product(cls, product):
        objects = cls.objects.filter(product=product)
        return objects

    @property
    def name(self):
        return f"{self.user} review of {self.product.name}"

    @property
    def short_description(self):
        return truncatewords(self.comment, 20)


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

    reaction = models.PositiveSmallIntegerField(choices=REACTIONS)

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

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    image = models.ImageField(
        upload_to="product_media_image", default="default_image/default_image.png"
    )

    class Meta:
        verbose_name_plural = _("Product image")

    def small_image_tag(self):
        return format_html(
            '<img href="{0}" src="{0}" width="50" height="50" />'.format(self.image.url)
        )

    @classmethod
    def get_media_by_product(cls, product):
        objects = cls.objects.filter(product=product)
        return objects

    # @classmethod
    # def get_all_products(cls, product_id = 1):
    #     objects = cls.objects.get(id != product_id)
    #     return objects

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

    class Meta:
        verbose_name_plural = _("Product video")

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="video_links",
    )

    video_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_media_video_by_product(cls, product):
        objects = cls.objects.filter(product=product)
        return objects

    @property
    def name(self):
        return f"Video {self.id} of {self.product}"


class AdvancedProductDescription(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
    )
    content = RichTextField()

    class Meta:
        verbose_name_plural = _("Product advanced description")
