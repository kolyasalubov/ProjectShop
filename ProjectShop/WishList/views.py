from rest_framework import viewsets, status
from rest_framework.response import Response

from ProductApp.models import Product
from WishList.serializers import WishListSerializer


class WishListViewSet(viewsets.ModelViewSet):
    """This is viewset for WishList"""
    serializer_class = WishListSerializer

    def get_serializer(self):
        return self.request.user.wishlist.all()

    def update(self, request, *args, **kwargs):
        product = Product.objects.get(id=request.data.get('product'))
        if product is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request.user.wishlist.add(product)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request):
        product = Product.objects.get(id=request.data.get('product'))
        if product is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request.user.wishlist.remove(product)
        return Response(status=status.HTTP_200_OK)
