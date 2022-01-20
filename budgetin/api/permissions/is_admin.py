from rest_framework import permissions
from api.exceptions import NotAuthorizedException


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request, 'custom_user'):
            if request.custom_user and request.custom_user['role'] == 'admin':
                return True
        raise NotAuthorizedException()
