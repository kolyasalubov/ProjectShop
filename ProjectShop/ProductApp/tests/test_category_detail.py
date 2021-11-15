from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve

from ProductApp.views import CategoryDetailView
from ProductApp.models import ProductCategory
from ProductApp.tests.factories import ProductCategoryFactory


class CategoryDetailTest(TestCase):

    def setUp(self):
        self.category = ProductCategoryFactory()
        url = reverse('category-detail', args=(self.category.slug,))
        self.response = self.client.get(url)

    def test_categories_detail_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_categories_detail_template(self):
        self.assertTemplateUsed(self.response,
                                'ProductApp/category_detail.html'
                                )

    def test_categories_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'I should not be on the page')

    def test_categories_detail_url_resolves_categories_detailview(self):
        view = resolve(f'/categories/{self.category.slug}/')
        self.assertEqual(view.func.__name__,
                         CategoryDetailView.as_view().__name__
                         )


class CategoryDetailViewTest(TestCase):

    def setUp(self):
        self.category = ProductCategoryFactory()
        request = RequestFactory().get(f'/categories/{self.category.slug}/')
        self.view = CategoryDetailView()
        self.view.setup(request)
        self.view.object = 1
        self.context = self.view.get_context_data()
        ProductCategoryFactory.create_batch(25)

    def test_attrs(self):
        self.assertEqual(self.view.model, ProductCategory)
        self.assertEqual(self.view.context_object_name, 'category_detail')
        self.assertEqual(self.view.template_name,
                         'ProductApp/category_detail.html'
                         )

    def test_environment_set_in_context(self):
        self.assertIn('products', self.context)
        self.assertIn('categories', self.context)

    def test_environment_set_not_in_context(self):
        self.assertNotIn('i_should_not_be_passed', self.context)

    def test_query_sets_categories(self):
        n = 20
        self.assertQuerysetEqual(self.context['categories'],
                                 ProductCategory.objects.order_by('name')[:n]
                                 )
        self.assertCountEqual(self.context['categories'],
                              ProductCategory.objects.order_by('name')[:n]
                              )
