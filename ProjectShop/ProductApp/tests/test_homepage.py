from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve

from ProductApp.views import HomePageView


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
    def test_environment_set_in_context(self):
        request = RequestFactory().get('/')
        view = HomePageView()
        view.object_list = ''
        view.setup(request)

        context = view.get_context_data()
        self.assertIn('products', context)
        self.assertIn('categories', context)
