from rest_framework import permissions


class IsBot(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (not user.role
                and user.phone.number == "+380666666666"
                and user.email == "bot@mail.com"
                and user.is_active)
