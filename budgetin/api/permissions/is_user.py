from rest_framework import permissions

from api.exceptions import NotAuthorizedException
from api.utils.enum import RoleEnum


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.custom_user and request.custom_user['role'] == RoleEnum.USER.value:
            return True
        raise NotAuthorizedException()
