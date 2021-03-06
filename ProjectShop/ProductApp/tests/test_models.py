from django.db.utils import IntegrityError
from django.template.defaultfilters import truncatewords
from django.test import TestCase

from ProductApp.tests.factories import (
    ProductFactory,
    ProductCategoryFactory,
    ProductSubcategoryFactory,
    TagFactory,
    TagGroupFactory,
    ReviewFactory,
)


class ProductTestCase(TestCase):
    """Test Case for Product model"""

    def setUp(self) -> None:
        self.product = ProductFactory()

    def test_name(self):
        product = self.product
        self.assertEqual(product.name, product.__str__())

    def test_categories_is_not_empty(self):
        product = self.product
        self.assertTrue(product.categories.all().exists())

    def test_subcategories_is_not_empty(self):
        product = self.product
        self.assertTrue(product.subcategories.all().exists())

    def test_tags_is_not_empty(self):
        product = self.product
        self.assertTrue(product.tags.all().exists())

    def test_category_create_add_clear(self):
        product = self.product
        self.assertTrue(product.categories.all().count() <= 5)
        for category in ProductCategoryFactory.create_batch(3):
            product.categories.add(category)
        self.assertFalse(product.categories.all().count() <= 2)
        product.categories.clear()
        self.assertTrue(product.categories.all().count() == 0)

    def test_short_description(self):
        product = self.product
        self.assertEqual(
            truncatewords(product.description, 20), product.short_description
        )


class ProductCategoryTestCase(TestCase):
    """Test Case for ProductCategory model"""

    def setUp(self) -> None:
        self.category = ProductCategoryFactory()

    def test_create(self):
        category = self.category
        self.assertIsNotNone(category)

    def test_str(self):
        category = self.category
        self.assertEqual(category.name, category.__str__())

    def test_create_with_no_name(self):
        category = ProductCategoryFactory(name="")
        self.assertIsNotNone(category)
        self.assertEqual(category.name, "")
        category.name = "cat1"
        category.save()
        self.assertNotEqual(category.name, "")

    def test_create_with_None_as_name(self):
        with self.assertRaises(IntegrityError):
            self.category = ProductCategoryFactory(name=None)


class ProductSubcategoryTestCase(TestCase):
    """Test Case for ProductSubcategory model"""

    def setUp(self) -> None:
        self.subcategory = ProductSubcategoryFactory()

    def test_create(self):
        subcategory = self.subcategory
        self.assertIsNotNone(subcategory)

    def test_str(self):
        subcategory = self.subcategory
        self.assertEqual(subcategory.name, subcategory.__str__())

    def test_create_with_no_name(self):
        subcategory = ProductSubcategoryFactory(name="")
        self.assertIsNotNone(subcategory)
        self.assertEqual(subcategory.name, "")
        subcategory.name = "subcat1"
        subcategory.save()
        self.assertNotEqual(subcategory.name, "")

    def test_create_with_None_as_name(self):
        with self.assertRaises(IntegrityError):
            self.subcategory = ProductSubcategoryFactory(name=None)


class TagGroupTestCase(TestCase):
    """Test Case for TagGroup model"""

    @classmethod
    def setUpTestData(cls):
        cls.group = TagGroupFactory()

    def test_create(self):
        self.assertIsNotNone(self.group)

    def test_str(self):
        self.assertEqual(self.group.name, str(self.group))

    def test_create_with_None_as_name(self):
        with self.assertRaises(IntegrityError):
            TagGroupFactory(name=None)


class TagTestCase(TestCase):
    """Test Case for Tag model"""

    def setUp(self) -> None:
        self.tag = TagFactory()

    def test_create(self):
        tag = self.tag
        self.assertIsNotNone(tag)

    def test_str(self):
        tag = self.tag
        self.assertEqual(tag.name, tag.__str__())

    def test_create_with_no_name(self):
        tag = TagFactory(name="")
        self.assertIsNotNone(tag)
        self.assertEqual(tag.name, "")
        tag.name = "tag1"
        tag.save()
        self.assertNotEqual(tag.name, "")

    def test_create_with_None_as_name(self):
        with self.assertRaises(IntegrityError):
            self.tag = TagFactory(name=None)


class ReviewTestCase(TestCase):
    """Test Case for Review model"""

    def setUp(self) -> None:
        self.review = ReviewFactory()

    def test_create(self):
        review = self.review
        self.assertIsNotNone(review)

    def test_str(self):
        review = self.review
        self.assertEqual(review.name, review.__str__())

    def test_rating(self):
        review = self.review
        self.assertTrue(0 <= review.rating <= 5)
        self.assertFalse(type(review.rating) == "str")
        # this raises Asserting error because we can
        # add any number to rating on edit, which is wrong
        with self.assertRaises(IntegrityError):
            review.rating = 6

    def test_is_active(self):
        review = self.review
        self.assertTrue(review.is_active)
        review.is_active = False
        review.save()
        self.assertFalse(review.is_active)

    def test_short_description(self):
        review = self.review
        self.assertEqual(truncatewords(review.comment, 20), review.short_description)
