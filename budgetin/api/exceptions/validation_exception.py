from rest_framework.exceptions import APIException


class ValidationException(APIException):
    status_code = 400
    default_detail = "Validation Error"
