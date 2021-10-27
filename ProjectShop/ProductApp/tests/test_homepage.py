from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve

from ProductApp.views import HomePageView
from ProductApp.models import Product, ProductCategory
from ProductApp.tests.factories import ProductCategoryFactory, ProductFactory


class HomePageTest(TestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'ProductApp/homepage.html')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class HomePageViewTest(TestCase):

    def setUp(self):
        request = RequestFactory().get('/')
        self.view = HomePageView()
        self.view.object_list = ''
        self.view.setup(request)
        self.context = self.view.get_context_data()
        ProductCategoryFactory.create_batch(25)
        ProductFactory.create_batch(20)

    def test_attrs(self):
        self.assertEqual(self.view.context_object_name, 'products')
        self.assertEqual(self.view.template_name, 'ProductApp/homepage.html')

    def test_environment_set_in_context(self):
        self.assertIn('products', self.context)
        self.assertIn('categories', self.context)

    def test_query_sets_categories(self):
        self.assertQuerysetEqual(self.context['categories'],
                                 ProductCategory.objects.order_by('name')[:20]
                                 )
        self.assertCountEqual(self.context['categories'],
                              ProductCategory.objects.order_by('name')[:20]
                              )

    def test_query_sets_products(self):
        self.assertQuerysetEqual(self.view.get_queryset(),
                                 Product.objects.all(),
                                 ordered=False
                                 )
        self.assertCountEqual(self.view.get_queryset(), Product.objects.all())
