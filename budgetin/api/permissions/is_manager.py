from rest_framework import permissions

from api.exceptions import NotEligibleException


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        eselon =  request.custom_user['eselon']
        if eselon == 'S1' or eselon == 'S2' or eselon == 'S3':
            return True
        raise NotEligibleException()