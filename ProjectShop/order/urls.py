from django.urls import path

from order.views import CartView, CartAddView
app_name = 'order'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('add/', CartAddView.as_view(), name='cart-add'),
    path('remove/', CartAddView.as_view(), name='cart-remove'),
    path('substract/', CartAddView.as_view(), name='cart-substract')
]