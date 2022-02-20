from rest_framework.exceptions import APIException


class FileNotFoundException(APIException):
    status_code = 500
    default_detail = 'Import template not found'