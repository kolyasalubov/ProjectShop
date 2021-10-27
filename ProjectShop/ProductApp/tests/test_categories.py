from django.test import TestCase
from django.urls import reverse, resolve

from ProductApp.views import CategoriesView
from ProductApp.models import ProductCategory
from ProductApp.tests.factories import ProductCategoryFactory


class CategoriesTest(TestCase):

    def setUp(self):
        url = reverse('categories')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'ProductApp/categories.html')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_homepage_url_resolves_categoriesview(self):
        view = resolve('/categories/')
        self.assertEqual(view.func.__name__, CategoriesView.as_view().__name__)


class CategoriesViewTest(TestCase):
    def setUp(self):
        request = RequestFactory().get('/')
        self.view = CategoriesView()
        self.view.setup(request)
        ProductCategoryFactory.create_batch(25)

    def test_attrs(self):
        self.assertEqual(self.view.model, ProductCategory)
        self.assertEqual(self.view.context_object_name, 'categories')
        self.assertEqual(self.view.template_name, 'ProductApp/categories.html')

    def test_query_sets_categories(self):
        self.assertQuerysetEqual(self.view.get_queryset(),
                                 ProductCategory.objects.all(),
                                 ordered=False
                                 )
        self.assertCountEqual(self.view.get_queryset(),
                              ProductCategory.objects.all(),
                              )
