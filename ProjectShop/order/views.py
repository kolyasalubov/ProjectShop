from django.views import generic, View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework import viewsets

from order.context_processors import SessionCart
from order.models import Order, OrderItems
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


class CartAddView(View):
    context_object_name = 'objects'
    template_name = 'order/order_page.html'

    def post(self, request, *args, **kwargs):
        cart = SessionCart(request)

        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('productId'))
            product = get_object_or_404(Product, id=product_id)

            qty, price = cart.add(product=product)
            response = JsonResponse({'qty': str(qty),
                                     'price': str(price)})

            return response

        elif request.POST.get('action') == 'remove':
            product_id = request.POST.get('productId')
            cart.remove(product_id)

            response = JsonResponse({'test': 'data'})

            return response

        elif request.POST.get('action') == 'substract':
            product_id = request.POST.get('productId')
            qty, price = cart.substract(product_id)

            response = JsonResponse({'qty': str(qty),
                                     'price': str(price),
                                     })

            return response