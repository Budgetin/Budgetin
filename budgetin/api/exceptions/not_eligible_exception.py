from rest_framework.exceptions import APIException


class NotEligibleException(APIException):
    status_code = 401
    default_detail = "You don't have access to Budgetin site."
