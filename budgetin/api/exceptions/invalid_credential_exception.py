from rest_framework.exceptions import APIException


class InvalidCredentialException(APIException):
    status_code = 401
    default_detail = "Invalid Credential. Please check your username and password."
