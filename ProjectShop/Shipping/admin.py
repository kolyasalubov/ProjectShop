from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from ProjectShop.custom_filters import DropdownChoicesFieldListFilter
from Shipping.models import ShippingModel


class ShippingModelAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    fields = ("user", "postal_code", "country", "region", "city", "post_office")
    list_display = ("user", "country", "city", "post_office")
    list_editable = ("post_office",)
    list_filter = (("country", DropdownChoicesFieldListFilter),)
    ordering = (
        "country",
        "region",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("user",)
        return self.readonly_fields


admin.site.register(ShippingModel, ShippingModelAdmin)
