from django.contrib import admin
from django.http import StreamingHttpResponse
from django.utils.translation import ugettext_lazy as _

import csv

from order.models import OrderModel, OrderItemsModel


class EchoCsv:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def order_to_list(order) -> list:
    """
    Function that returns row for export_to_csv method in order/admin.py
    """
    order_object = OrderModel.objects.get(id=order['id'])
    user_object = order_object.user
    shipping_address_object = order_object.shippingAddress_id

    order_items_objects = OrderItemsModel.objects.filter(order=order['id'])
    product_list = []
    for order_item in order_items_objects:
        quantity = order_item.order_items_qantity
        product = str(order_item.product)

        product_list.append(f'{product}:{quantity}')
    products = ' ; '.join(product_list)

    order_row = [order_object.payment_method, order_object.payment_status, str(shipping_address_object),
                  str(user_object), products]

    return order_row


@admin.action(description=_('Export orders data to csv format'))
def export_to_csv(modeladmin, request, queryset):
    rows = (order_to_list(query) for query in queryset.values('id', ))
    pseudo_buffer = EchoCsv()
    writer = csv.writer(pseudo_buffer, delimiter=';')

    writer.writerow(['Payment method', 'Payment status', 'Shipping address', 'User data', 'Products'])

    return StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv",
        headers={'Content-Disposition': 'attachment; filename="orders.csv"'},
    )
