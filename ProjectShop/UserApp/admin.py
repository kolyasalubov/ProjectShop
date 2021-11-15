from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from import_export.admin import ImportExportActionModelAdmin

from UserApp.models import User


class UserAdmin(ImportExportActionModelAdmin, BaseUserAdmin):
    def has_delete_permission(self, request, obj=None) -> bool:
        """Restrict self deletion and deletion for not superusers"""

        return request.user != obj and request.user.is_superuser

    def has_add_permission(self, request) -> bool:
        """Restrict adding for not superusers"""

        return request.user.is_superuser

    def has_change_permission(self, request, obj=None) -> bool:
        """Allow changing for superusers and for admin to change users"""

        return request.user.role

    def get_form(self, request, obj=None, **kwargs):
        """Enable certain fields in form"""

        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        enabled_fields = set()  # type Set[str]

        if is_superuser:
            enabled_fields |= set(
                form.base_fields.keys()
            )  # going to enable all fields except "role"
            if obj:
                enabled_fields.remove(
                    "role"
                )  # disable to choose role if changing any User
                enabled_fields.remove(
                    "is_bot"
                )  # disable to choose is_bot if changing any User
            if obj == request.user:
                enabled_fields.remove("is_active")  # disable to change is_active

        elif request.user.role and obj and not obj.role:
            enabled_fields |= {
                "is_active"
            }  # enable for admin to change is_active for user

        elif obj == request.user:
            enabled_fields |= {
                "middle_name",
                "birth_date",
            }  # enable for admin to change middle_name and birth_date

        for field in form.base_fields:
            if field in enabled_fields:
                continue
            form.base_fields[
                field
            ].disabled = True  # disable form fields except enabled fields
        return form

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = (
        "phone_number",
        "first_name",
        "last_name",
        "role",
        "email",
        "is_active",
        "register_date",
        "is_superuser",
        "is_bot",
        "telegram_id",
    )
    list_filter = ("is_superuser", "is_active", "role")
    fieldsets = (
        (None, {"fields": ("phone_number", "wishlist", )}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "birth_date",
                    "email",
                    "role",
                    "profile_pic",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_bot")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "email",
                    "role",
                    "password1",
                    "password2",
                    "is_bot",
                ),
            },
        ),
    )
    search_fields = ("phone_number",)
    ordering = ("phone_number",)
    filter_horizontal = ("wishlist",)


# registering new django admin...
admin.site.register(User, UserAdmin)
# unregistering the Group model from admin.
admin.site.unregister(Group)

admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)
