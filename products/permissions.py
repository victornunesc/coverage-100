from rest_framework import permissions


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if request.user.is_authenticated:
                return request.user.is_seller

            return False

        return True
