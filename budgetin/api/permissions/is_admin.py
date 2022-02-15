from rest_framework import permissions

from api.exceptions import NotAuthorizedException
from api.utils.enum import RoleEnum


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.custom_user and request.custom_user['role'] == RoleEnum.ADMIN.value:
            return True
        raise NotAuthorizedException()
