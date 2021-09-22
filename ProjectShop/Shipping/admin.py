from django.contrib import admin
from Shipping.models import ShippingModel


class ShippingModelAdmin(admin.ModelAdmin):
    fields = ('user', 'postal_code', 'country', 'region', 'city', 'post_office')
    list_display = ('user', 'country', 'city', 'post_office')
    list_editable = ('post_office',)
    search_fields = ('country', )  # doesnt work ????
    ordering = ('country', 'region',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields


admin.site.register(ShippingModel, ShippingModelAdmin)
