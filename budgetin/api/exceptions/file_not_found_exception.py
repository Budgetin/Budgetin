from rest_framework.exceptions import APIException


class FileNotFoundException(APIException):
    status_code = 400
    default_detail = "File not found."