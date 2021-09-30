from django.test import TestCase
from django.db.utils import IntegrityError

from ProductApp.tests.factories import *


class ProductTestCase(TestCase):
	def setUp(self) -> None:
		pass

	def test_name(self):
		product = ProductFactory()
		self.assertEqual(product.name, product.__str__())

	def test_categories_is_not_empty(self):
		product = ProductFactory()
		self.assertNotEqual(product.categories.all(), [])

	def test_subcategories_is_not_empty(self):
		product = ProductFactory()
		self.assertNotEqual(product.subcategories.all(), [])

	def test_tags_is_not_empty(self):
		product = ProductFactory()
		self.assertNotEqual(product.tags.all(), [])

	def test_category_create_add_clear(self):
		product = ProductFactory()
		self.assertTrue(product.categories.all().count() <= 5)
		for category in ProductCategoryFactory.create_batch(3):
			product.categories.add(category)
		self.assertFalse(product.categories.all().count() <= 2)
		product.categories.clear()
		self.assertTrue(product.categories.all().count() == 0)

	def test_shot_description(self):
		product = ProductFactory()
		self.assertEqual(product.short_description, truncatewords(product.description, 20))
		product.description = 'This is 20symbol description' + product.description
		self.assertEqual(product.short_description[:20], 'This is 20symbol des')


class ProductCategoryTestCase(TestCase):
	def setUp(self) -> None:
		pass

	def test_create(self):
		category = ProductCategoryFactory()
		self.assertIsNotNone(category)

	def test_str(self):
		category = ProductCategoryFactory()
		self.assertEqual(category.name, category.__str__())

	def test_create_with_no_name(self):
		category = ProductCategoryFactory(name='')
		self.assertIsNotNone(category)
		self.assertEqual(category.name, '')
		category.name = 'cat1'
		self.assertNotEqual(category.name, '')

	def test_create_with_None_as_name(self):
		try:
			category = ProductCategoryFactory(name=None)
		except IntegrityError:
			self.assertTrue(True)


class ProductSubcategoryTestCase(TestCase):
	def setUp(self) -> None:
		pass

	def test_create(self):
		subcategory = ProductSubcategoryFactory()
		self.assertIsNotNone(subcategory)

	def test_str(self):
		subcategory = ProductSubcategoryFactory()
		self.assertEqual(subcategory.name, subcategory.__str__())

	def test_create_with_no_name(self):
		subcategory = ProductSubcategoryFactory(name='')
		self.assertIsNotNone(subcategory)
		self.assertEqual(subcategory.name, '')
		subcategory.name = 'subcat1'
		self.assertNotEqual(subcategory.name, '')

	def test_create_with_None_as_name(self):
		try:
			subcategory = ProductSubcategoryFactory(name=None)
		except IntegrityError:
			self.assertTrue(True)


class TagTestCase(TestCase):
	def setUp(self) -> None:
		pass

	def test_create(self):
		tag = TagFactory()
		self.assertIsNotNone(tag)

	def test_str(self):
		tag = TagFactory()
		self.assertEqual(tag.name, tag.__str__())

	def test_create_with_no_name(self):
		tag = TagFactory(name='')
		self.assertIsNotNone(tag)
		self.assertEqual(tag.name, '')
		tag.name = 'tag1'
		self.assertNotEqual(tag.name, '')

	def test_create_with_None_as_name(self):
		try:
			tag = TagFactory(name=None)
		except IntegrityError:
			self.assertTrue(True)


class ProductMediaTestCase(TestCase):
	def setUp(self) -> None:
		pass

	def test_create(self):
		media = ProductMediaFactory()
		self.assertIsNotNone(media)

	def test_str(self):
		media = ProductMediaFactory()
		self.assertEqual(media.name, media.__str__())
		print(media.name)

	def test_media_type(self):
		media = ProductMediaFactory()
		self.assertTrue(media.media_type <= 1)

	def test_url(self):
		media = ProductMediaFactory()
		self.assertIn('http', media.video_link)
		self.assertIn('://', media.video_link)


class ReviewTestCase(TestCase):
	def setUp(self) -> None:
		pass

	def test_create(self):
		review = ReviewFactory()
		self.assertIsNotNone(review)

	def test_str(self):
		review = ReviewFactory()
		self.assertEqual(review.name, review.__str__())
		print(review.name)

	def test_rating(self):
		review = ReviewFactory()
		self.assertTrue(0 <= review.rating <= 5)
		self.assertFalse(type(review.rating) == 'str')
		try:
			review.rating = 6
		except IntegrityError:
			self.assertTrue(True)

	def test_is_active(self):
		review = ReviewFactory()
		self.assertTrue(review.is_active)
		review.disable()
		self.assertFalse(review.is_active)

	def test_short_description(self):
		review = ReviewFactory()
		self.assertEqual(review.short_description, truncatewords(review.comment, 20))
		review.comment = 'Hello world' + review.comment
		self.assertEqual(review.short_description[:11], 'Hello world')
