from rest_framework import permissions

from api.exceptions import NotAuthenticatedException


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request, 'custom_user'):
            return True
        raise NotAuthenticatedException()
