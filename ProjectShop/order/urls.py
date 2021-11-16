from django.urls import path

from order.views import CartView, CartAddView, CartRemoveView, CartSubtractView
# from order.views import MakeAnOrder, OrderConfirmation

app_name = 'order'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('add/', CartAddView.as_view(), name='cart-add'),
    path('remove/', CartRemoveView.as_view(), name='cart-remove'),
    path('subtract/', CartSubtractView.as_view(), name='cart-subtract'),
    # path('checkout/', MakeAnOrder.as_view(), name='checkout'),
    # path('order-confirmation/', OrderConfirmation.as_view(), name="order-confirmation"),
]
