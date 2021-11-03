from django.views import View
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from braces.views import AjaxResponseMixin, JSONResponseMixin

from django.views import generic
from rest_framework import viewsets

from order.context_processors import SessionCart
from order.models import Order, OrderItems
from ProductApp.models import Product
from order.serializers import OrderDetailSerializer, OrderItemsSerializer
from ProductApp.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    """This is viewset for order model"""

    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    http_method_names = ["post", "get", "patch", "put"]


class OrderItemsViewSet(viewsets.ModelViewSet):
    """This is viewset for order items model"""

    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    http_method_names = ["post", "get", "patch", "put"]


class CartView(generic.ListView):
    context_object_name = 'objects'
    template_name = 'order/order_page.html'

    def get_queryset(self):
        return SessionCart(self.request).list()


class CartAddView(JSONResponseMixin, AjaxResponseMixin, View):
    http_method_names = ('post', )

    def post_ajax(self, request, *args, **kwargs):
        cart = SessionCart(request)

        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        qty, price = cart.add(product=product)
        response = {'qty': str(qty), 'price': str(price)}

        return self.render_json_response(response)


class CartRemoveView(JSONResponseMixin, AjaxResponseMixin, View):
    http_method_names = ('post', )

    def post_ajax(self, request, *args, **kwargs):
        cart = SessionCart(request)

        product_id = request.POST.get('productId')
        cart.remove(product_id)

        return self.render_json_response({})


class CartSubtractView(JSONResponseMixin, AjaxResponseMixin, View):
    http_method_names = ('post', )

    def post_ajax(self, request, *args, **kwargs):
        cart = SessionCart(request)

        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        qty, price = cart.subtract(product)

        response = {'qty': str(qty), 'price': str(price)}

        return self.render_json_response(response)


class MakeAnOrder(CartView):
    context_object_name = 'objects'

    template_name = "order/make_order.html"

    def get_queryset(self):
        return SessionCart(self.request).list()


class OrderConfirmation(TemplateView):
    template_name = "order/order_confirmation.html"