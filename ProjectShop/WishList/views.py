from django.utils.translation import gettext as _

from rest_framework import viewsets, status
from rest_framework.response import Response

from UserApp.models import User
from ProductApp.models import Product
from WishList.serializers import WishListSerializer


class WishListViewSet(viewsets.ModelViewSet):
    serializer_class = WishListSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        product = Product.objects.filter(id=request.data.get('product'))
        if not product:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(product)
        return Response(data={'message': _('Item updated successfully!')}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        product = Product.objects.filter(id=request.data.get('product'))
        if not product:
            return Response(data={'message': _('Product with such id doesn\'t exist.')}, status=status.HTTP_204_NO_CONTENT)
        self.perform_destroy(product)
        return Response(data={'message': _('Wishlist item deleted successfully!')}, status=status.HTTP_200_OK)
