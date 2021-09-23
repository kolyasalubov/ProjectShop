from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

import csv

from Shipping.models import ShippingModel
from order.models import OrderModel, OrderItemsModel


@admin.action(description=_('Export orders data to csv format'))
def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Payment method', 'Payment status', 'Shipping address', 'User data', 'Products'])

    orders = queryset.values('id', 'payment_method', 'payment_status', 'shippingAddress_id', 'user',)

    for order in orders:
        user_data = str(OrderModel.objects.get(id=order['id']).user)
        shipping_address = str(ShippingModel.objects.get(id=order['shippingAddress_id']))

        order_items = OrderItemsModel.objects.filter(order=order['id'])
        product_list = []
        for order_item in order_items:
            quantity = order_item.order_items_qantity
            product = str(order_item.product)

            product_list.append(f'{product}:{quantity}')

        order_list = [order['payment_method'], order['payment_status'], shipping_address,
                      user_data, ' ; '.join(product_list)]
        writer.writerow(order_list)

    return response


class OrderItemsInline(admin.TabularInline):
    model = OrderItemsModel
    readonly_fields = ('order_items_qantity', 'product')
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    fields = ('user', 'payment_method', 'shipping_status', 'payment_status', 'shippingAddress_id', 'order_date')
    readonly_fields = ('order_date', )
    inlines = (OrderItemsInline, )
    list_display = ('user', 'payment_status', 'shipping_status', )
    list_editable = ('payment_status', 'shipping_status', )
    list_filter = ('payment_status', 'shipping_status', )
    ordering = ('payment_status', 'shipping_status', )
    actions = (export_to_csv, )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user', 'payment_method', 'shippingAddress_id')
        return self.readonly_fields


class OrderItemsAdmin(admin.ModelAdmin):
    fields = ('order_items_qantity', 'order', 'product')
    readonly_fields = ('product', 'order_items_qantity', 'order')
    list_display = ('product', 'order_items_qantity', 'order')
    list_filter = ('product', )
    ordering = ('product', 'order', )


admin.site.register(OrderModel, OrderAdmin)
admin.site.register(OrderItemsModel, OrderItemsAdmin)

