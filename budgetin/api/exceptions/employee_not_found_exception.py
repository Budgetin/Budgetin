from rest_framework.exceptions import APIException


class EmployeeNotFoundException(APIException):
    status_code = 404
    default_detail = "Employee Data Not Found."
