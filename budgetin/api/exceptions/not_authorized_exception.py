from rest_framework.exceptions import APIException


class NotAuthorizedException(APIException):
    status_code = 403
    default_detail = "You are not authorized to access this api."
