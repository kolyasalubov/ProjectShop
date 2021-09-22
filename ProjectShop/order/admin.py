from django.contrib import admin

from order.models import OrderModel, OrderItemsModel


class OrderItemsInline(admin.TabularInline):
    model = OrderItemsModel
    readonly_fields = ('order_items_qantity',)
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    fields = ('user', 'payment_method', 'shipping_status', 'payment_status', 'shippingAddress_id', 'order_date')
    readonly_fields = ('order_date', )
    inlines = (OrderItemsInline, )
    list_display = ('user', 'payment_status', 'shipping_status', )
    list_editable = ('payment_status', 'shipping_status', )
    list_filter = ('payment_status', 'shipping_status', )
    ordering = ('payment_status', 'shipping_status', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user', 'payment_method', 'shippingAddress_id')
        return self.readonly_fields


admin.site.register(OrderModel, OrderAdmin)
admin.site.register(OrderItemsModel)

