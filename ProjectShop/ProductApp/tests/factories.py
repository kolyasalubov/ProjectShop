import factory
from factory import fuzzy
import random

from ProductApp.models import (Product, ProductCategory, ProductSubcategory,
							   ProductMedia, Tag, Review)


class TagFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Tag

	name = factory.Faker('word')


class ProductCategoryFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = ProductCategory

	name = factory.Faker('word')


class ProductSubcategoryFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = ProductSubcategory

	name = factory.Faker('word')


class ProductFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Product

	name = factory.Faker('word')
	price = factory.Faker('random_int', min=100, max=5000)
	description = factory.Faker('text')
	stock_quantity = factory.Faker('random_int', min=0, max=100)
	#categories = set(['one', 'two'])
	#subcategories = ['three', 'four']
	#tags = ['five', 'six']

	@factory.post_generation
	def categories(self, create, extracted, **kwargs):
		if not create:
			self.categories.add(['one', 'two'])
			# Simple build, do nothing.
			return

		if extracted:
			# A list of groups were passed in, use them
			for category in extracted:
				self.categories.add(category)

	@factory.post_generation
	def subcategories(self, create, extracted, **kwargs):
		if not create:
			self.subcategories.add(['three', 'four'])
			return

		if extracted:
			# A list of groups were passed in, use them
			for subcategory in extracted:
				self.subcategories.add(subcategory)

	@factory.post_generation
	def tags(self, create, extracted, **kwargs):
		if not create:
			self.tags.add(['five', 'six'])
			return

		if extracted:
			# A list of groups were passed in, use them
			for tag in extracted:
				self.tags.add(tag)


class ProductMediaFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = ProductMedia


class ReviewFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Review


