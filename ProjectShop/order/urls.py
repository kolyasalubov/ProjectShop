from django.urls import path

from order.views import CartView, CartAddView, CartRemoveView, CartSubtractView
app_name = 'order'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('add/', CartAddView.as_view(), name='cart-add'),
    path('remove/', CartRemoveView.as_view(), name='cart-remove'),
    path('substract/', CartSubtractView.as_view(), name='cart-subtract')
]