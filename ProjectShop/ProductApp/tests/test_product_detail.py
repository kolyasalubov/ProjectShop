from django.test import TestCase
from django.urls import reverse, resolve

from ProductApp.tests.factories import ProductFactory
from ProductApp.views import ProductDetailView
from ProductApp.models import Product


class ProductDetailTest(TestCase):

    def setUp(self):
        self.product = ProductFactory()
        url = reverse("product-detail", args=(self.product.slug,))
        self.response = self.client.get(url)

    def test_product_detail_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_product_detail_template(self):
        self.assertTemplateUsed(self.response,
                                "ProductApp/product_detail.html"
                                )

    def test_product_detail_contains_correct_html(self):
        self.assertContains(self.response, f"{self.product}")
        self.assertContains(self.response, f"{self.product.price}")
        self.assertContains(self.response, f"{self.product.description}")

    def test_product_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "I should not be on the page")

    def test_product_detail_url_resolves_product_datailview(self):
        view = resolve(f"/{self.product.slug}/")
        self.assertEqual(view.func.__name__,
                         ProductDetailView.as_view().__name__
                         )


class ProductDetailViewTest(TestCase):

    def setUp(self):
        self.view = ProductDetailView()

    def test_attrs(self):
        self.assertEqual(self.view.model, Product)
        self.assertEqual(self.view.context_object_name, "product_detail")
        self.assertEqual(self.view.template_name,
                         "ProductApp/product_detail.html"
                         )
