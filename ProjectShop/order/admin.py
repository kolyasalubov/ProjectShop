from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

import csv

from order.models import OrderModel, OrderItemsModel
from order.export import export_to_csv
from ProjectShop.custom_filters import MultipleChoiceListFilter


class ShippingStatusListFilter(MultipleChoiceListFilter):
    title = _('shipping status')
    parameter_name = 'shipping_status__in'

    def lookups(self, request, model_admin):
        return OrderModel.ShippingStatus.choices


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
    list_filter = ('payment_status', ShippingStatusListFilter, )
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

