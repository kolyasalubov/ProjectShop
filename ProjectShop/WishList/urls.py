from django.urls import path

from WishList.views import WishListViewSet

urlpatterns = [
    path('user/wishlist/', WishListViewSet.as_view(), name='wishlist')
]
