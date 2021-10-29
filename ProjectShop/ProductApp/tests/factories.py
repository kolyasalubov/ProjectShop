import random

import factory

from ProductApp.models import (
    Product,
    ProductCategory,
    ProductSubcategory,
    Tag,
    Review,
)
from UserApp.tests.factories import UserFactory


class TagFactory(factory.django.DjangoModelFactory):
    """Factory for Tag model"""

    class Meta:
        model = Tag

    name = factory.Faker("word")


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    """Factory for ProductCategory model"""

    class Meta:
        model = ProductCategory

    name = factory.Faker("word")


class ProductSubcategoryFactory(factory.django.DjangoModelFactory):
    """Factory for ProductSubcategory model"""

    class Meta:
        model = ProductSubcategory

    name = factory.Faker("word")


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory for Product model"""

    class Meta:
        model = Product

    name = factory.Faker("word")
    price = factory.Faker("random_int", min=100, max=5000)
    description = factory.Faker("text")
    stock_quantity = factory.Faker("random_int", min=0, max=100)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        categories = (
            extracted
            if extracted is not None
            else ProductCategoryFactory.create_batch(random.randint(1, 5))
        )
        for category in categories:
            self.categories.add(category)

    @factory.post_generation
    def subcategories(self, create, extracted, **kwargs):
        subcategories = (
            extracted
            if extracted is not None
            else ProductSubcategoryFactory.create_batch(random.randint(1, 5))
        )
        for subcategory in subcategories:
            self.subcategories.add(subcategory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        tags = (
            extracted
            if extracted is not None
            else TagFactory.create_batch(random.randint(1, 5))
        )
        for tag in tags:
            self.tags.add(tag)


class ReviewFactory(factory.django.DjangoModelFactory):
    """Factory for Review model"""

    class Meta:
        model = Review

    rating = factory.Faker("random_int", min=0, max=5)
    comment = factory.Faker("text")
    is_active = True

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
