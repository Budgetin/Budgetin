from rest_framework.exceptions import APIException


class NotAuthenticatedException(APIException):
    status_code = 401
    default_detail = "You have to login first."
